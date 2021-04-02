import pytest

from churchill.apps.core.utils import get_dates_for_weeks_count
from churchill.tests.factories.users import UserFactory


@pytest.mark.django_db
class TestUtils:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.user = UserFactory()

    def test_get_dates_for_weeks_count(self):
        date_range = get_dates_for_weeks_count(self.user)
        assert len(list(date_range)) == 7 * 4

        date_range = get_dates_for_weeks_count(self.user, weeks_count=6)
        assert len(list(date_range)) == 7 * 6

        date_range = get_dates_for_weeks_count(self.user, weeks_count=2, weeks_offset=2)
        assert len(list(date_range)) == 7 * 2
