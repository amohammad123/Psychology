from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import generics, status, views, mixins
from rest_framework import permissions
from rest_framework import filters
from django.db.models import Case, When, IntegerField

from conf.time import time_now
from conf.functions import (get_sub_ids, Ordering)
from conf.pagination import (CustomCategoriesItemPagination)
from account.permissions import ClientPermission

from package.v1.serializers import (CategoriesPackageSerializer)
from post.models import Category
from package.models import Package


class CategoriesPackageApiView(generics.ListAPIView):
    """
    this view get the posts of each category
    """
    # permission_classes = [permissions.IsAuthenticated] # todo: uncomment
    serializer_class = CategoriesPackageSerializer
    lookup_url_kwarg = 'category_id'
    pagination_class = CustomCategoriesItemPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'tags']
    search_fields = ['name', 'category__name', 'tags__name', 'user__first_name', 'user__last_name', 'summary',
                     'description', 'prerequisite', 'rates__comment']

    def get_queryset(self):
        category_id = self.kwargs.get(self.lookup_url_kwarg)
        category = Category.objects.get(id=category_id)
        ides = get_sub_ids(obj_id=category_id, obj=category, parent_field='parents_category')
        queryset = Package.objects.all().filter(category__in=ides, is_deleted=False, index=0)
        queryset = Ordering(request=self.request, queryset=queryset, category_id=category_id).get_order()

        return queryset
