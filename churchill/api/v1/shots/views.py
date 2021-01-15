from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response

from churchill.api.v1.shots.serializers import ShotSerializer, ShotItemSerializer
from churchill.apps.shots.models import Shot, ShotItem
from churchill.apps.shots.services import create_shot, delete_shot, delete_shot_item, create_shot_item


class ShotsView(CreateAPIView, DestroyAPIView, ListAPIView):

    serializer_class = ShotSerializer

    def get_queryset(self):
        return Shot.objects.for_user(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shot = create_shot(request.user, **serializer.validated_data)
        serializer = self.get_serializer(shot)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        delete_shot(request.user, request.data["id"])
        return Response()


class ShotsItemView(CreateAPIView, DestroyAPIView, ListAPIView):

    serializer_class = ShotItemSerializer

    def get_queryset(self):
        return ShotItem.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            shot = Shot.objects.for_user(self.request.user).get(id=request.data["id"])
        except Shot.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        shot_item = create_shot_item(request.user, shot)
        serializer = self.get_serializer(shot_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        delete_shot_item(request.user, request.data["id"])
        return Response()
