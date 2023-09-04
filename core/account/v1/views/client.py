from rest_framework.response import Response
from rest_framework import generics, status, views, mixins
from rest_framework import permissions

from conf.time import time_now
from account.permissions import ClientPermission
from account.v1.serializers.profile import SetProfileSerializer
from account.models.profile import Profile


class SetProfileApiView(generics.GenericAPIView):
    queryset = Profile.objects.all()
    # permission_classes = [ClientPermission]  # todo: uncomment
    serializer_class = SetProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(context={'request': request}, data=request.data)
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'message': 'کاربر با موفقیت ساخته شد', 'user': serializer.data})
