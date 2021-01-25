from datetime import timedelta

from dateutil.tz import UTC
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

import pytest

from faker import Faker

from churchill.tests.factories.shots import ShotItemFactory
from churchill.tests.factories.users import UserFactory


@pytest.mark.django_db
class TestShotsCalendarView:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("api:v1:shots:calendar")
        self.user = UserFactory()
        self.faker = Faker()

    def test_anonymous_user(self):
        response = self.client.get(self.url, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize("method", ["post", "put", "patch"])
    def test_not_allowed_methods(self, method):
        self.client.force_authenticate(self.user)
        test_client_callable = getattr(self.client, method)
        response = test_client_callable(self.url, format="json")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_shots_calendar(self):
        self.client.force_authenticate(self.user)

        start_date = timezone.now() - timedelta(weeks=4)
        for _ in range(7):
            shot_item = ShotItemFactory(user=self.user)
            shot_item.created_at = self.faker.date_time_between(
                start_date=start_date, tzinfo=UTC
            )
            shot_item.save()

        response = self.client.get(self.url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert (
            len(list(filter(lambda x: x["is_drunk"], response.json()["results"]))) == 7
        )
