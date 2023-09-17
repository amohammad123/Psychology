from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, views, mixins
from rest_framework import permissions

from django.db.models import Case, When, IntegerField

from conf.time import time_now
from conf.functions import get_sub_ids
from account.permissions import ClientPermission

from post.v1.serializers.post import (CategoriesPostSerializer)
from post.models import Post, Category


class CategoriesPostApiView(generics.ListAPIView):
    """
    this view get the posts of each category
    """
    # permission_classes = [permissions.IsAuthenticated] # todo: uncomment
    serializer_class = CategoriesPostSerializer
    lookup_url_kwarg = 'category_id'

    def get_queryset(self):
        category_id = self.kwargs.get(self.lookup_url_kwarg)
        category = Category.objects.get(id=category_id)
        ides = get_sub_ids(obj_id=category_id, obj=category, parent_field='parents_category')
        queryset = Post.objects.all().filter(category__in=ides, is_deleted=False, status='published').annotate(
            custom_order=Case(
                When(category=category_id, then=1),
                default=2,
                output_field=IntegerField()
            )
        ).order_by('custom_order', '-create_date')
        return queryset
