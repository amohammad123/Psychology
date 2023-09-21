from django.urls import path

from post.v1.views.post import (CategoriesPostApiView, TagIdsApiView)

urlpatterns = [
    # get all posts of category
    path('category/<uuid:category_id>/posts', CategoriesPostApiView.as_view(), name='category-posts'),
    path('tags', TagIdsApiView.as_view(), name='Tags'),
    # set trappist profile
    # path('set/trappist', TrappistSetProfileApiView.as_view(), name='set-trappist-profile'),
]