import base64

from rest_framework import serializers
from rest_framework.response import Response

from conf.model import MyModelSerializer
from django.core import exceptions
from django.db.models import Avg

from account.v1.serializers.profile import BaseProfileSerializer
from conf.time import time_now

from conf.serializer_functions import (SerializerItems)
from package.models import Package, PackageFile, PackagePayment, PackageRate
from account.models.profile import Profile
from account.v1.serializers.profile import BaseProfileSerializer
from post.v1.serializers.post import BaseTagSerializer, TagIdsSerializer
from post.v1.serializers.category import BaseCategorySerializer


class PackageFileSerializer(MyModelSerializer):
    class Meta:
        model = PackageFile
        fields = ['id', 'file', 'is_main']

    def to_representation(self, instance):
        if not instance.is_deleted:
            return super().to_representation(instance)
        else:
            return None


class PackagePaymentSerializer(MyModelSerializer):
    class Meta:
        model = PackagePayment
        fields = ['original_price', 'offer_price', 'get_percent']
        read_only_fields = ['get_percent']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep


class PackageLikeSerializer(MyModelSerializer):
    class Meta:
        model = PackageRate
        fields = ['like']


class PackageCommentSerializer(MyModelSerializer):
    user = BaseProfileSerializer(read_only=True, required=False)

    class Meta:
        model = PackageRate
        fields = ['id', 'user', 'comment', 'like', 'create_date']
        # read_only_fields = ['user', 'id']

    def create(self, validated_data):
        user = 'eea6e8e7-34e2-4ad2-96fa-d80977ae4226'
        # user = '8a9ff596-1cb0-4a91-b55e-0114cc2df157'

        user = Profile.objects.get(user=user)
        # todo: uncomment this
        # user = self.context.get('request').user.id
        # user = Profile.objects.get(user=user)

        package_id = self.context.get('package_id')
        package = PackageRate.objects.create(user=user, package_id=package_id, **validated_data)
        return package

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        create_data = round((time_now() - instance.create_date) / 60)
        rep['create_date'] = create_data
        return rep


class CategoriesPackageSerializer(MyModelSerializer):
    user = BaseProfileSerializer()
    category = BaseCategorySerializer(many=True)
    tags = BaseTagSerializer(many=True)

    class Meta:
        model = Package
        exclude = ['is_deleted', 'create_date', 'update_date', 'parent_package']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['files'] = PackageFileSerializer(instance.files.filter(is_deleted=False, is_main=True), many=True).data

        # rep['rate'] = instance.rates.all().aggregate(rate=Avg('rate'))['rate'] or 0
        rep['like_count'] = instance.rates.filter(like=True).count()
        rep['comment_count'] = instance.rates.filter(comment__isnull=False).count()
        rep['price'] = PackagePaymentSerializer(instance.payment.filter(is_deleted=False), many=True).data

        return rep


class PackageSerializer(MyModelSerializer):
    """
    this serializer get all package by index 0 & create package by index 0
    """
    tags = serializers.ListSerializer(child=serializers.CharField(), required=False)
    category = serializers.ListSerializer(child=serializers.CharField(), required=False)
    files = serializers.ListSerializer(child=serializers.JSONField(), required=False)
    payment = PackagePaymentSerializer(required=False)

    class Meta:
        model = Package
        fields = ['parent_package', 'id', 'name', 'summary', 'description', 'prerequisite', 'order', 'category', 'tags',
                  'files', 'payment']

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
        parent_package = validated_data.pop('parent_package', None)
        category_ids = validated_data.pop('category', [])
        tags_data = validated_data.pop('tags', [])
        files = validated_data.pop('files', [])
        price = validated_data.pop('payment', None)
        tags = SerializerItems(tags=tags_data).add_tags()

        package = Package.objects.create(user=self.get_user, parent_package=parent_package, **validated_data)

        SerializerItems(files=files, queryset=package, method='create').add_file()
        if price is not None:
            SerializerItems(price=price, queryset=package, method='create').add_payment()

        package.tags.set(tags)
        package.category.set(category_ids)
        return package

    def update(self, instance, validated_data):
        files = validated_data.get('files', None)
        tags = validated_data.get('tags', None)
        category = validated_data.get('category', None)
        price = validated_data.pop('payment', None)

        if files is not None:
            SerializerItems(files=files, queryset=instance, method='update').add_file()

        if tags is not None:
            tags = SerializerItems(tags=tags).add_tags()
            instance.tags.clear()
            instance.tags.set(tags)

        if category is not None:
            instance.category.clear()
            instance.category.set(category)

        if price is not None:
            SerializerItems(price=price, queryset=instance, method='update').add_payment()

        instance.name = validated_data.get('name', instance.name)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.description = validated_data.get('description', instance.description)
        instance.prerequisite = validated_data.get('prerequisite', instance.prerequisite)
        instance.save()

        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['files'] = PackageFileSerializer(instance.files.filter(is_deleted=False), many=True).data
        rep['time'] = instance.time
        rep['views'] = instance.views
        rep['sell_count'] = instance.sell_count
        rep['category'] = BaseCategorySerializer(instance.category.filter(is_deleted=False), many=True).data
        rep.pop('payment')
        rep['price'] = PackagePaymentSerializer(instance.payment.filter(is_deleted=False), many=True).data
        rep['like_count'] = instance.rates.filter(like=True).count()
        rep['comment_count'] = instance.rates.filter(comment__isnull=False).count()
        if instance.parents_package is not None:
            rep['sub_package'] = PackageSerializer(
                Package.objects.filter(parent_package=str(rep['id'])).order_by('order', '-create_date'),
                many=True).data
            obj = rep['sub_package']
            for sub in obj:
                sub.pop('price')
                sub.pop('sell_count')
                sub.pop('category')
            if len(rep['sub_package']) == 0:
                rep.pop('sub_package')
        return rep
