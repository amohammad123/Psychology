from django.urls import path, include
urlpatterns = [
    path('v1/', include('exam.v1.urls')),
]