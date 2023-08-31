from django.urls import path, include
urlpatterns = [
    path('v1/', include('post.v1.urls')),
]