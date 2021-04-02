from dateutil.tz import UTC
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

import pytest

from faker import Faker

from churchill.apps.core.utils import get_dates_for_weeks_count
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

        oldest_shots = []
        newest_shots = []
        date_range = list(get_dates_for_weeks_count(self.user, 8))
        start_date = date_range[0]
        end_date = date_range[-1]
        middle_date = start_date + (end_date - start_date) / 2
        for _ in range(15):
            shot_item = ShotItemFactory(user=self.user)
            shot_item.created_at = self.faker.date_time_between(
                start_date=start_date, tzinfo=UTC
            )
            shot_item.save()

            if shot_item.created_at > middle_date:
                newest_shots.append(shot_item)
            else:
                oldest_shots.append(shot_item)

        response = self.client.get(self.url, format="json")
        assert response.status_code == status.HTTP_200_OK
        response_dates = list(
            filter(lambda x: x["is_drunk"], response.json()["results"])
        )
        shot_dates = set([x.created_at.date() for x in newest_shots])
        assert len(response_dates) == len(shot_dates)

        response = self.client.get(f"{self.url}?weeks_offset=4", format="json")
        assert response.status_code == status.HTTP_200_OK
        response_dates = list(
            filter(lambda x: x["is_drunk"], response.json()["results"])
        )
        shot_dates = set([x.created_at.date() for x in oldest_shots])
        assert len(response_dates) == len(shot_dates)
