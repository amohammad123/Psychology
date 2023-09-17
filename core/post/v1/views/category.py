from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, views, mixins
from rest_framework import permissions

from conf.time import time_now
from account.permissions import ClientPermission
from post.v1.serializers.category import (ListCategorySerializer, DetailCategorySerializer, SubDetailCategorySerializer,
                                          CategoryDetailSerializer)
from post.models import Category


# todo: complete this view for create category by admin
# class CreateCategoryApiView(generics.CreateAPIView):
#     # permission_classes = [permissions.IsAdminUser] # todo: uncomment
#     serializer_class = ListCategorySerializer
#     queryset = Category.objects.all()

class ListCategoryApiView(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]  # todo: uncomment
    serializer_class = ListCategorySerializer
    queryset = Category.objects.all().filter(index=0, parent_category__isnull=True, is_deleted=False)


class DetailCategoryApiView(generics.ListAPIView):
    """
    this view get the sub categories by index 1

    """
    # permission_classes = [permissions.IsAuthenticated] # todo: uncomment
    serializer_class = DetailCategorySerializer
    queryset = Category.objects.all().filter(parent_category__isnull=True, is_deleted=False)


class SubDetailCategoryApiView(generics.ListAPIView):
    """
    this view get the whole sub categories
    """
    # permission_classes = [permissions.IsAuthenticated] # todo: uncomment
    serializer_class = SubDetailCategorySerializer
    queryset = Category.objects.all().filter(parent_category__isnull=True, is_deleted=False)


class CategoryDetailApiView(generics.RetrieveAPIView):
    """
    this view get the detail of each category
    """
    # permission_classes = [permissions.IsAuthenticated] # todo: uncomment
    serializer_class = CategoryDetailSerializer
    lookup_url_kwarg = 'category_id'
    queryset = Category.objects.all().filter(is_deleted=False)

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.context = {'request': self.request}
        return super().get_serializer(*args, **kwargs)
