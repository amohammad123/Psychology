from django.urls import path
from account.v1.views.client import SetProfileApiView

urlpatterns = [
    path('set', SetProfileApiView.as_view(), name='set-profile'),
]