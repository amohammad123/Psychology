from rest_framework import serializers
from conf.model import MyModelSerializer
from django.core import exceptions
from django.db.models import Avg

from post.models import (Category, Post, Tag, PostRate)
from account.models.profile import Profile
from account.v1.serializers.profile import BaseProfileSerializer
from .category import BaseCategorySerializer
from conf.serializer_functions import (SerializerItems)


class BaseTagSerializer(MyModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # rep['rate'] =
        return rep


class CategoriesPostSerializer(MyModelSerializer):
    author = BaseProfileSerializer()
    category = BaseCategorySerializer()
    tags = BaseTagSerializer(many=True)

    class Meta:
        model = Post
        exclude = ['is_deleted', 'create_date', 'update_date', 'published_date', 'comment_status', 'body']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # rep['rate'] = instance.rates.all().aggregate(rate=Avg('rate'))['rate'] or 0
        rep['like_count'] = instance.rates.filter(like=True).count()
        rep['comment_count'] = instance.comments.filter(is_enable=True).count()
        return rep


# class TagIdsSerializer(serializers.Serializer):
#     tags = serializers.ListSerializer(child=serializers.CharField())
#
#     def create(self, validated_data):
#         tag_names = validated_data.get('tags', [])
#         tag_ids = []
#         for tag_name in tag_names:
#             tag, created = Tag.objects.get_or_create(name=tag_name)
#             tag_ids.append(tag.id if tag is not None else created.id)
#         validated_data['tags'] = tag_ids
#         return validated_data


class PostSerializer(MyModelSerializer):
    tags = serializers.ListSerializer(child=serializers.CharField(), required=False)
    category = serializers.CharField()
    files = serializers.ListSerializer(child=serializers.JSONField(), required=False)

    # author = BaseProfileSerializer(read_only=True)
    # category = BaseCategorySerializer(read_only=True)
    # tags = BaseTagSerializer(many=True)

    class Meta:
        model = Post
        exclude = ['update_date', 'is_deleted']
        read_only_fields = ['views', 'author']

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

    def create(self, validated_data, *args, **kwargs):
        category_id = validated_data.pop('category')
        files = validated_data.pop('files')
        tags_data = validated_data.pop('tags')
        tags = SerializerItems(tags=tags_data).add_tags()

        category = Category.objects.get(id=category_id)
        post = Post.objects.create(author=self.get_user, category_id=category.id, **validated_data)
        SerializerItems(files=files, queryset=post, method='create').add_file()
        post.tags.set(tags)

        return PostSerializer(post).data
