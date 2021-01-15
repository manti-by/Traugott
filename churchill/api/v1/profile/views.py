import logging

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response

from churchill.api.v1.profile.serializers import ProfileSerializer
from churchill.apps.profiles.services import update_profile

logger = logging.getLogger()


class ProfileView(RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user.profile)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = update_profile(request.user.profile, **serializer.validated_data)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class ProfileImageView(CreateAPIView):

    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        try:
            image = request.data["image"]
        except KeyError:
            logger.warning("Request has no image attached")
            raise ValidationError("Request has no image attached")
        request.user.profile.image = image
        request.user.profile.save()
        serializer = self.get_serializer(request.user.profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
