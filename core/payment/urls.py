from django.urls import path, include
urlpatterns = [
    path('v1/', include('payment.v1.urls')),
]