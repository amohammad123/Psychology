from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from account.v1.views.user import TokenObtainCustomPairView, GetCodeApiView, CodeVerificationApiView

app_name = "accounts"

urlpatterns = [
    # get_code
    path('code/send', GetCodeApiView.as_view(), name='code-submit'),  # phase 1/sign up 9
    # code verification
    path('code/verification', CodeVerificationApiView.as_view(), name='code-login'),  # phase 1/sign up 10

    # sign up
    # path('signup', SignUpApiView.as_view(), name='signup'),

    # registration
    # path("registration", RegistrationGenerics.as_view(), name="registration"),
    # path("test-email", TestEmailApiView.as_view(), name="test email"),

    # activation
    # path(
    #     "activation/confirm/<str:token>",
    #     ActivationApiView.as_view(),
    #     name="activation-confirm",
    # ),

    # resend activation
    # path(
    #     "activation/resend", ActivationResendApiView.as_view(), name="activation-resend"
    # ),

    # change password
    # path("change-password", ChangePasswordApiView.as_view(), name="change-password"),

    # reset password

    # login jwt
    # path("jwt/access", TokenObtainPairView.as_view(), name="jwt-access"),
    path("jwt/access", TokenObtainCustomPairView.as_view(), name="jwt-access"),
    path("jwt/refresh", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify", TokenVerifyView.as_view(), name="jwt-verify"),
]
