from django.urls import path
from account.v1.views.client import SetProfileApiView
from account.v1.views.trappist import TrappistSetProfileApiView

urlpatterns = [
    # set client profile
    path('set/client', SetProfileApiView.as_view(), name='set-client-profile'),
    # set trappist profile
    path('set/trappist', TrappistSetProfileApiView.as_view(), name='set-trappist-profile'),
]