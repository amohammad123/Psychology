from django.urls import path, include
urlpatterns = [
    path('v1/', include('prescription.v1.urls')),
]