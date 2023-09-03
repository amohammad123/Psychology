from rest_framework.response import Response
from rest_framework import generics, status, views, mixins
from rest_framework import permissions

from conf.time import time_now
from account.v1.serializers.profile import SetProfileSerializer


class SetProfileApiView(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]  # todo: uncomment
    serializer_class = SetProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(context={'request': request}, data=request.data)
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
