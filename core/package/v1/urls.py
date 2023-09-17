from django.urls import path

from package.v1.views import (CategoriesPackageApiView)

urlpatterns = [
    path('category/<uuid:category_id>/packages', CategoriesPackageApiView.as_view(), name='category-packages'),
]
