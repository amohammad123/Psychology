from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse

from rest_framework import generics, status, views, mixins
from rest_framework import permissions

from account.v1.serializers.user import (TokenObtainCustomPairSerializer, GetCodeSerializer, CodeVerificationSerializer,
                                         SetPasswordSerializer, ChangePasswordSerializer)
from account.models.user import CustomUser, PhoneCode
from conf.time import time_now


class TokenObtainCustomPairView(TokenObtainPairView):
    """
    custom token jwt
    """
    serializer_class = TokenObtainCustomPairSerializer

    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        if 'access' in res.data:
            res.set_cookie(key='access_token', value=res.data['access'], httponly=True)
        return res


class GetCodeApiView(generics.GenericAPIView):
    serializer_class = GetCodeSerializer
    queryset = PhoneCode.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class SignUpApiView(generics.GenericAPIView):
#     serializer_class = SignUpSerializer
#     queryset = CustomUser.objects.all()
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if not serializer.is_valid():
#             return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         serializer.save()
#         return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)


class CodeVerificationApiView(generics.GenericAPIView):
    serializer_class = CodeVerificationSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)


class SetPasswordApiView(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]  # todo: uncomment
    serializer_class = SetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'user': serializer.data, 'message': 'رمز عبور با موفقیت ساخته شد'},
                        status=status.HTTP_201_CREATED)


class ResetPasswordApiView(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]  # todo: uncomment
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = self.serializer_class(context={"request": request}, data=request.data)
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'user': serializer.data, 'message': 'رمز عبور با موفقیت تغییر یافت'},
                        status=status.HTTP_200_OK)
