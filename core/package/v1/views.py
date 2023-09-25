from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import generics, status, views, mixins, viewsets
from rest_framework import permissions
from rest_framework import filters

from conf.time import time_now
from conf.functions import (get_sub_ids, Ordering)
from conf.pagination import (CustomItemPagination)
from account.permissions import ClientPermission

from package.v1.serializers import (CategoriesPackageSerializer, PackageSerializer, PackageCommentSerializer)
from post.models import Category
from package.models import Package, PackageRate


class CategoriesPackageApiView(generics.ListAPIView):
    """
    this view get the posts of each category
    """
    # permission_classes = [permissions.IsAuthenticated] # todo: uncomment
    serializer_class = CategoriesPackageSerializer
    lookup_url_kwarg = 'category_id'
    pagination_class = CustomItemPagination
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


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all().filter(is_deleted=False)
    serializer_class = PackageSerializer
    pagination_class = CustomItemPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'tags']
    search_fields = ['name', 'category__name', 'tags__name', 'user__first_name', 'user__last_name', 'summary',
                     'description', 'prerequisite', 'rates__comment']

    def list(self, request, *args, **kwargs):
        """
        get all packages by index 0
        """
        self.serializer_class = CategoriesPackageSerializer
        self.queryset = Package.objects.all().filter(index=0, is_deleted=False)
        self.queryset = Ordering(request=self.request, queryset=self.queryset, category_id=None).get_order()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.get_object().viewed()
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({'message': 'پکیج با موفقیت حذف شد'}, status=status.HTTP_200_OK)


class PackageCommentListView(generics.ListCreateAPIView):
    serializer_class = PackageCommentSerializer
    pagination_class = CustomItemPagination
    lookup_field = 'package_id'

    def get_queryset(self):
        package_id = self.kwargs.get('package_id')
        return PackageRate.objects.filter(package_id=package_id, is_deleted=False).order_by('-create_date')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request, 'package_id': self.kwargs.get('package_id')})
        return context

# class CreateMainPackageApiView(generics.CreateAPIView):
#     """
#     this view create package
#     """
#     # permission_classes = [permissions.IsAuthenticated] # todo: uncomment
#     serializer_class = ParentPackageSerializer
#     queryset = Package.objects.all()
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context.update({'request': self.request})
#         return context
