from django.urls import path
from post.v1.views.category import (ListCategoryApiView, DetailCategoryApiView, SubDetailCategoryApiView,
                                    CategoryDetailApiView)

urlpatterns = [
    # get parent categories
    path('list', ListCategoryApiView.as_view(), name='parent-category'),
    # get the sub categories by index 1
    path('detail', DetailCategoryApiView.as_view(), name='sub-category'),
    # get the whole sub categories
    path('sub/detail', SubDetailCategoryApiView.as_view(), name='sub-detail-category'),
    # get each category detail
    path('<uuid:category_id>', CategoryDetailApiView.as_view(), name='detail-category'),
]
