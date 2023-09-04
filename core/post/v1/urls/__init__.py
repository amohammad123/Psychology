from django.urls import path, include

urlpatterns = [
    path("category/", include("post.v1.urls.category")),
    path("post/", include("post.v1.urls.post")),
]
