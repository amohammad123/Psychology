from rest_framework import serializers
from conf.model import MyModelSerializer
from django.core import exceptions

from post.models import (Category, Post, Tag)
from account.v1.serializers.profile import BaseProfileSerializer
from .category import BaseCategorySerializer


class BaseTagSerializer(MyModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class CategoriesPostSerializer(MyModelSerializer):
    author = BaseProfileSerializer()
    category = BaseCategorySerializer()
    tags = BaseTagSerializer(many=True)

    class Meta:
        model = Post
        exclude = ['is_deleted', 'create_date', 'update_date']

