import logging

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
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


class ProfilesImageView(CreateAPIView):

    serializer_class = ProfilesSerializer

    def create(self, request, *args, **kwargs):
        try:
            image = request.data["image"]
        except KeyError:
            raise ValidationError("Request has no image attached")
        request.user.profile.image = image
        request.user.profile.save()
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
