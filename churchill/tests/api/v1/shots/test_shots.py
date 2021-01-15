from decimal import Decimal

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

import pytest

from churchill.apps.shots.models import Shot
from churchill.tests.factories.shots import ShotDictFactory, ShotFactory
from churchill.tests.factories.users import UserFactory


@pytest.mark.django_db
class TestShotsView:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("api:v1:shots:shots")
        self.user = UserFactory()
        self.shot_data = ShotDictFactory()

    def test_anonymous_user(self):
        response = self.client.get(self.url, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("method", ["put", "patch"])
    def test_not_allowed_methods(self, method):
        self.client.force_authenticate(self.user)
        test_client_callable = getattr(self.client, method)
        response = test_client_callable(self.url, format="json")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_shot_list(self):
        self.client.force_authenticate(self.user)

        ShotFactory()
        response = self.client.get(self.url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0

        ShotFactory(is_public=True, is_approved=True)
        response = self.client.get(self.url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

        ShotFactory(created_by=self.user)
        response = self.client.get(self.url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

    def test_create_and_delete_shot(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, self.shot_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == self.shot_data["title"]
        assert response.data["volume"] == self.shot_data["volume"]
        assert response.data["volume"] == self.shot_data["volume"]
        assert Decimal(response.data["cost"]) == self.shot_data["cost"]
        assert Shot.objects.exists()

        response = self.client.delete(
            self.url, {"id": [Shot.objects.first().id]}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert not Shot.objects.exists()
