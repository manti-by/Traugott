from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

import pytest

from churchill.tests.factories.shots import ShotFactory, ShotItemFactory
from churchill.tests.factories.users import UserFactory


@pytest.mark.django_db
class TestProfileStatsView:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("api:v1:profile:profile")
        self.user = UserFactory()

    def test_retrieve_stats_data(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert not response.data["stats"]

        shot = ShotFactory()
        shot_item = ShotItemFactory(shot=shot, user=self.user)
        response = self.client.get(self.url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["stats"]["last_shot_at"] == shot_item.created_at
        assert response.data["stats"]["timedelta_last_shot"]
