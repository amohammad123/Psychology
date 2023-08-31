from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import generics
from rest_framework import mixins

from account.v1.serilizers.user import TokenObtainCustomPairSerializer, GetCodeSerializer
from account.models.user import CustomUser, PhoneCode
from conf.time import time_now


class TokenObtainCustomPairView(TokenViewBase):
    """
    custom token jwt
    """
    serializer_class = TokenObtainCustomPairSerializer


class GetCodeApiView(generics.GenericAPIView):
    serializer_class = GetCodeSerializer
    queryset = PhoneCode.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({'message': serializer.error})
        serializer.save()
        return Response(serializer.data)

class Login():
    pass
