from django.urls import path, include
from rest_framework.routers import DefaultRouter

from post.v1.views.post import (CategoriesPostApiView, PostViewSet)

router = DefaultRouter()
router.register(r'post', PostViewSet)

urlpatterns = [
    # get all posts of category
    path('category/<uuid:category_id>/posts', CategoriesPostApiView.as_view(), name='category-posts'),
    # path('tags', TagIdsApiView.as_view(), name='Tags'),
    path('', include(router.urls))
]