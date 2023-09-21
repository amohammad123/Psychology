import base64

from rest_framework import serializers
from rest_framework.response import Response

from conf.model import MyModelSerializer
from django.core import exceptions
from django.db.models import Avg

from account.v1.serializers.profile import BaseProfileSerializer
from package.models import Package, PackageFile, PackagePayment, PackageRate
from account.models.profile import Profile
from account.v1.serializers.profile import BaseProfileSerializer
from post.v1.serializers.post import BaseTagSerializer, TagIdsSerializer
from post.v1.serializers.category import BaseCategorySerializer


class CategoriesPackageSerializer(MyModelSerializer):
    user = BaseProfileSerializer()
    category = BaseCategorySerializer(many=True)
    tags = BaseTagSerializer(many=True)

    class Meta:
        model = Package
        exclude = ['is_deleted', 'create_date', 'update_date', 'parent_package']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # rep['rate'] = instance.rates.all().aggregate(rate=Avg('rate'))['rate'] or 0
        rep['like_count'] = instance.rates.filter(like=True).count()
        rep['comment_count'] = instance.rates.filter(comment__isnull=False).count()

        return rep


class PackageFileSerializer(MyModelSerializer):
    class Meta:
        model = PackageFile
        fields = ['file']


class PackagePaymentSerializer(MyModelSerializer):
    class Meta:
        model = PackagePayment
        exclude = ['package', 'is_deleted', 'create_date', 'update_date']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['percent'] = instance.get_percent()
        return rep


class PackageLikeSerializer(MyModelSerializer):
    class Meta:
        model = PackageRate
        fields = ['like']


class DetailPackageSerializer(MyModelSerializer):
    tags = serializers.ListSerializer(child=serializers.CharField(), required=False)
    category = serializers.ListSerializer(child=serializers.CharField(), required=False)
    files = PackageFileSerializer(many=True)

    class Meta:
        model = Package
        fields = ['id', 'name', 'summary', 'description', 'prerequisite', 'category', 'tags', 'files']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            # todo: uncomment this
            # self.user = self.context.get('request').user.id
            # if not self.user.is_authenticated:
            #     raise serializers.ValidationError({'message': 'کاربر وارد نشده است'})
            self.user = 'eea6e8e7-34e2-4ad2-96fa-d80977ae4226'
            # self.user = '8a9ff596-1cb0-4a91-b55e-0114cc2df157'
            self.get_user = Profile.objects.get(user_id=self.user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError({'message': 'کاربر با این مشخصات یافت نشد'})

    def validate(self, attrs):
        if not self.get_user.is_trappist:
            raise serializers.ValidationError('کاربر باید درمانگر باشد')
        return attrs

    def create(self, validated_data):
        category_ids = validated_data.pop('category', [])
        tags_data = validated_data.pop('tags', [])
        files = validated_data.pop('files', [])
        tag_serializer = TagIdsSerializer(data={'tags': tags_data})
        tag_serializer.is_valid(raise_exception=True)
        tag_serializer.save()
        tags = tag_serializer.data.get('tags')

        package = Package.objects.create(user=self.get_user, index=0, **validated_data)
        if len(files) > 0:

            for file in files:
                PackageFile.objects.create(file=file, package=package)
        package.tags.set(tags)
        package.category.set(category_ids)
        return package

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['time'] = instance.time
        rep['views'] = instance.views
        rep['sell_count'] = instance.sell_count
        rep['category'] = BaseCategorySerializer(instance.category, many=True).data
        rep['price'] = PackagePaymentSerializer(instance.payment, many=True).data
        rep['like_count'] = instance.rates.filter(like=True).count()
        rep['comment_count'] = instance.rates.filter(comment__isnull=False).count()
        return rep
