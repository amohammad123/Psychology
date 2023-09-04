from rest_framework.response import Response
from rest_framework import generics, status, views, mixins
from rest_framework import permissions

from conf.time import time_now
from account.permissions import TrappistPermission
from account.v1.serializers.profile import TrappistSetProfileSerializer
from account.models.profile import Profile


class TrappistSetProfileApiView(generics.GenericAPIView):
    queryset = Profile.objects.all()
    # permission_classes = [TrappistPermission]  # todo: uncomment
    serializer_class = TrappistSetProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(context={'request': request}, data=request.data)
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'message': 'کاربر با موفقیت ساخته شد', 'user': serializer.data})
