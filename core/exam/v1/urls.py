from django.urls import path

from exam.v1.views import (CategoriesTestApiView)

urlpatterns = [
    path('category/<uuid:category_id>/tests', CategoriesTestApiView.as_view(), name='category-tests'),
]