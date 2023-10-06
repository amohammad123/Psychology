# from post.v1.serializers.post import TagIdsSerializer
from post.models import Tag, PostFile
from package.models import Package, PackageFile, PackagePayment
from rest_framework import serializers


class TagIdsSerializer(serializers.Serializer):
    tags = serializers.ListSerializer(child=serializers.CharField())

    def create(self, validated_data):
        tag_names = validated_data.get('tags', [])
        tag_ids = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_ids.append(tag.id if tag is not None else created.id)
        validated_data['tags'] = tag_ids
        return validated_data


class SerializerItems:
    def __init__(self, queryset=None, method=None, tags=None, files=None, price=None):
        self.queryset = queryset
        self.model = queryset.__class__.__name__
        self.method = method
        self.tags = tags
        self.files = files
        self.price = price
        self.tag_serializer = TagIdsSerializer(data={'tags': tags})
        if price is not None:
            self.original_price = price.get('original_price')
            self.offer_price = price.get('offer_price')

    def add_tags(self):
        tag_serializer = self.tag_serializer
        tag_serializer.is_valid(raise_exception=True)
        tag_serializer.save()
        tags = tag_serializer.data.get('tags')
        return tags

    def add_file(self):
        if self.method == 'create':
            for file in self.files:
                file_data = file.get('file', None)
                is_main = file.get('is_main', None)
                if self.model == 'Package':
                    create_file = PackageFile.objects.create(file=file_data, package=self.queryset)
                if self.model == 'Post':
                    create_file = PostFile.objects.create(file=file_data, post=self.queryset)
                if is_main is not None:
                    create_file.is_main = True
                    create_file.save()
        if self.method == 'update':
            for file in self.files:
                file_id = file.get('id', None)
                file_data = file.get('file', None)
                is_main = file.get('is_main', None)
                if file_id is None and file_data is not None:
                    if self.model == 'Package':
                        create_file = PackageFile.objects.create(package_id=self.queryset.id, **file)
                    if self.model == 'Post':
                        create_file = PostFile.objects.create(post_id=self.queryset.id, **file)
                    if is_main is not None:
                        if self.model == 'Package':
                            PackageFile.objects.filter(package_id=self.queryset.id, is_deleted=False,
                                                       is_main=True).update(
                                is_main=False)
                        if self.model == 'Post':
                            PostFile.objects.filter(post_id=self.queryset.id, is_deleted=False, is_main=True).update(
                                is_main=False)
                        create_file.is_main = True
                        create_file.save()

                if file_data is None and file_id is not None:
                    if self.model == 'Package':
                        if is_main is not None:
                            PackageFile.objects.filter(package_id=self.queryset.id, is_deleted=False,
                                                       is_main=True).update(
                                is_main=False)
                            get_file = PackageFile.objects.get(id=file_id)
                            get_file.is_main = True
                            get_file.save()
                        else:
                            package_file = PackageFile.objects.get(id=file_id)
                            package_file.is_deleted = True
                            package_file.save()

                    if self.model == 'Post':
                        if is_main is not None:
                            PostFile.objects.filter(post_id=self.queryset.id, is_deleted=False,
                                                    is_main=True).update(
                                is_main=False)
                            get_file = PostFile.objects.get(id=file_id)
                            get_file.is_main = True
                            get_file.save()
                        else:
                            post_file = PostFile.objects.get(id=file_id)
                            post_file.is_deleted = True
                            post_file.save()

    def add_payment(self):
        if self.method == 'create':
            PackagePayment.objects.create(package=self.queryset, original_price=self.original_price,
                                          offer_price=self.offer_price)
        if self.method == 'update':
            self.queryset.payment.update(is_deleted=True)
            PackagePayment.objects.create(package=self.queryset, original_price=self.original_price,
                                          offer_price=self.offer_price)
