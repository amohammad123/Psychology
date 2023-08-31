from django.urls import path, include

urlpatterns = [
    path("", include("account.v1.urls.user")),
    path("profile/", include("account.v1.urls.profile")),
]