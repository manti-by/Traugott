from typing import Iterable
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now


def get_first_week_day_offset(user: User) -> int:
    return 0 if user.profile.language == "ru-ru" else 1


def date_range(start_date: datetime, end_date: datetime) -> Iterable[datetime]:
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_dates_for_weeks_count(
    user: User, weeks_count: int = settings.CALENDAR_WEEK_SIZE, weeks_offset: int = 0
) -> Iterable[datetime]:
    first_day_offset = get_first_week_day_offset(user)
    end_date = now() + timedelta(
        days=6 - datetime.now().isoweekday() + first_day_offset
    )
    start_date = end_date - timedelta(weeks=weeks_count)
    if weeks_offset:
        start_date = start_date - timedelta(weeks=weeks_offset)
        end_date = end_date - timedelta(weeks=weeks_offset)
    return date_range(start_date, end_date)
