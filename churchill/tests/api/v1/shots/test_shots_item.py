from decimal import Decimal

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

import pytest

from churchill.apps.shots.models import Shot, ShotItem
from churchill.tests.factories.shots import ShotFactory, ShotItemFactory
from churchill.tests.factories.users import UserFactory


@pytest.mark.django_db
class TestShotsItemView:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("api:v1:shots:item")
        self.user = UserFactory()
        self.shot = ShotFactory(created_by=self.user)

    def test_anonymous_user(self):
        response = self.client.get(self.url, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("method", ["put", "patch"])
    def test_not_allowed_methods(self, method):
        self.client.force_authenticate(self.user)
        test_client_callable = getattr(self.client, method)
        response = test_client_callable(self.url, format="json")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_shots_item_list(self):
        self.client.force_authenticate(self.user)

        ShotItemFactory()
        response = self.client.get(self.url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0

        ShotItemFactory(user=self.user)
        response = self.client.get(self.url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_create_and_delete_shot_item(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {"id": self.shot.id}, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert ShotItem.objects.exists()

        response = self.client.delete(
            self.url, {"id": [response.data["id"]]}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert not ShotItem.objects.exists()
