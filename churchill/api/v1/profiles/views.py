import logging

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from churchill.api.v1.profiles.serializers import ProfilesSerializer
from churchill.apps.profiles.services import update_profile

logger = logging.getLogger()


class ProfilesView(RetrieveUpdateAPIView):

    serializer_class = ProfilesSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = update_profile(request.user, **serializer.validated_data["profile"])
        serializer = self.get_serializer(instance.user)
        return Response(serializer.data)
