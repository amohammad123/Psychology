from rest_framework import serializers
from conf.model import MyModelSerializer
from django.core import exceptions

from post.models import (Category, Post)
from package.models import Package
from exam.models import Test
from conf.functions import (get_sub_ids)


# todo: complete this serializer for create category by admin

# class CreateCategorySerializer(MyModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'
#         read_only_fields = ['is_deleted', 'update_date']
#
#     def validate(self, attrs):
#         parent_category = attrs.get('parent_category')
#         parent_index = Category.objects.get(id=parent_category).indext
#         if attrs.get('index') <= parent_index:
#             raise serializers.ValidationError({'message': 'دسته بندی پدر انتخاب شده اشتباه است'})
#         return attrs
#
#     def create(self, validated_data):
#         for parent in validated_data:
#             Category.objects.create(**parent)
#
#         return validated_data

class BaseCategorySerializer(MyModelSerializer):
    class Meta:
        model = Category
        exclude = ['is_deleted', 'update_date', 'create_date']


class ListCategorySerializer(MyModelSerializer):
    class Meta:
        model = Category
        exclude = ['is_deleted', 'update_date', 'create_date']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop('parent_category', None)
        return rep


class DetailCategorySerializer(MyModelSerializer):
    """
    this serializer get the sub categories by index 1
    """

    class Meta:
        model = Category
        exclude = ['is_deleted', 'update_date', 'create_date']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['sub_category'] = DetailCategorySerializer(Category.objects.filter(index=1, parent_category=str(rep['id'])),
                                                       many=True).data
        if len(rep['sub_category']) == 0:
            rep.pop('sub_category')
        return rep


class SubDetailCategorySerializer(MyModelSerializer):
    """
    this serializer get the whole sub categories
    """

    class Meta:
        model = Category
        exclude = ['is_deleted', 'update_date', 'create_date']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['sub_category'] = SubDetailCategorySerializer(Category.objects.filter(parent_category=str(rep['id'])),
                                                          many=True).data
        if len(rep['sub_category']) == 0:
            rep.pop('sub_category')
        return rep


class CategoryDetailSerializer(MyModelSerializer):
    """
    this serializer get the detail of each category
    """

    class Meta:
        model = Category
        exclude = ['is_deleted', 'update_date', 'create_date']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            category_id = rep['id']
            category = Category.objects.get(id=category_id)
            rep['sub_category'] = BaseCategorySerializer(Category.objects.filter(parent_category=category_id),
                                                         many=True).data
            # rep['posts_count'] = category.posts.all().count()
            fiter_query = {
                'category__in': get_sub_ids(obj_id=category_id, obj=category, parent_field='parents_category'),
                'is_deleted': False}
            rep['posts_count'] = Post.objects.filter(status='published', **fiter_query).count()
            rep['tests_count'] = Test.objects.filter(**fiter_query, index=0).count()
            rep['packages_count'] = Package.objects.filter(**fiter_query, index=0).count()
            rep['categories_count'] = category.parents_category.all().count()
        except Category.DoesNotExist:
            raise serializers.ValidationError({'message': 'دسته بندی مورد نظر یافت نشد'})
        return rep
