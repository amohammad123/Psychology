from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, views, mixins, viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Case, When, IntegerField

from conf.time import time_now
from conf.functions import (get_sub_ids, Ordering)
from conf.pagination import (CustomItemPagination)

from account.permissions import ClientPermission
from post.v1.serializers.post import (CategoriesPostSerializer, PostSerializer)
from post.models import Post, Category, Tag


class CategoriesPostApiView(generics.ListAPIView):
    """
    this view get the posts of each category
    """
    # permission_classes = [permissions.IsAuthenticated] # todo: uncomment
    serializer_class = CategoriesPostSerializer
    lookup_url_kwarg = 'category_id'
    pagination_class = CustomItemPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'comment_status', 'tags']
    search_fields = ['title', 'category__name', 'body', 'author__first_name', 'author__last_name', 'rates__comment']

    def get_queryset(self):
        category_id = self.kwargs.get(self.lookup_url_kwarg)
        category = Category.objects.get(id=category_id)
        ides = get_sub_ids(obj_id=category_id, obj=category, parent_field='parents_category')
        queryset = Post.objects.all().filter(category__in=ides, is_deleted=False, status='published')
        queryset = Ordering(request=self.request, queryset=queryset, category_id=category_id).get_order()

        return queryset


# class TagIdsApiView(generics.CreateAPIView):
#     queryset = Tag.objects.all()
#     serializer_class = TagIdsSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().filter(is_deleted=False)
    serializer_class = PostSerializer
    pagination_class = CustomItemPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'comment_status', 'tags']
    search_fields = ['title', 'category__name', 'body', 'author__first_name', 'author__last_name', 'rates__comment']

    def list(self, request, *args, **kwargs):
        self.serializer_class = CategoriesPostSerializer
        self.queryset = Post.objects.all().filter(is_deleted=False, status='published')
        self.queryset = Ordering(request=self.request, queryset=self.queryset, category_id=None).get_order()
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        self.get_object().viewed()
        return super().retrieve(request, *args, **kwargs)
