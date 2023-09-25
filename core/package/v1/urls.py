from django.urls import path, include
from rest_framework.routers import DefaultRouter

from package.v1.views import (CategoriesPackageApiView, PackageViewSet, PackageCommentListView)

router = DefaultRouter()
router.register(r'package', PackageViewSet)

urlpatterns = [
    path('category/<uuid:category_id>/packages', CategoriesPackageApiView.as_view(), name='category-packages'),
    # path('package/create', CreateMainPackageApiView.as_view(), name='create-packages'),
    path('', include(router.urls)),
    path('package/<uuid:package_id>/comments', PackageCommentListView.as_view(), name='package-comments'),

]
