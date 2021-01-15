from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response

from churchill.api.v1.shots.serializers import ShotSerializer
from churchill.apps.shots.models import Shot
from churchill.apps.shots.services import create_shot, delete_shot


class ShotsView(CreateAPIView, DestroyAPIView, ListAPIView):

    serializer_class = ShotSerializer

    def get_queryset(self):
        return Shot.objects.filter(
            Q(created_by=self.request.user) | Q(is_public=True, is_approved=True)
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shot = create_shot(request.user, **serializer.validated_data)
        serializer = self.get_serializer(shot)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        delete_shot(request.user, request.data["id"])
        return Response()
