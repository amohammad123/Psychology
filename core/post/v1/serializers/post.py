from rest_framework import serializers
from conf.model import MyModelSerializer
from django.core import exceptions
from django.db.models import Avg

from post.models import (Category, Post, Tag, PostRate)
from account.v1.serializers.profile import BaseProfileSerializer
from .category import BaseCategorySerializer


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
        exclude = ['is_deleted', 'create_date', 'update_date', 'published_date', 'comment_status']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # rep['rate'] = instance.rates.all().aggregate(rate=Avg('rate'))['rate'] or 0
        rep['like_count'] = instance.rates.filter(like=True).count()
        rep['comment_count'] = instance.comments.filter(is_enable=True).count()
        return rep


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
