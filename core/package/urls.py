from django.urls import path, include
urlpatterns = [
    path('v1/', include('package.v1.urls')),
]