from decimal import Decimal
from typing import Optional

from django.conf import settings
from django.contrib.auth.models import User

from churchill.apps.core.utils import get_dates_for_weeks_count
from churchill.apps.shots.models import Shot, ShotItem


def create_shot(
    user: User, title: str, volume: int, degree: int, cost: Optional[Decimal] = 0.0
) -> Shot:
    return Shot.objects.create(
        title=title, volume=volume, degree=degree, cost=cost, created_by=user
    )


def delete_shot(user: User, id_list: list):
    Shot.objects.filter(id__in=id_list, created_by=user).delete()


def create_shot_item(user: User, shot: Shot) -> ShotItem:
    return ShotItem.objects.create(user=user, shot=shot)


def delete_shot_item(user: User, id_list: list):
    ShotItem.objects.filter(id__in=id_list, user=user).delete()


def get_shots_calendar(user: User) -> list:
    result = []
    shot_item_dates = list(
        map(
            lambda x: x.date(),
            ShotItem.objects.filter(user=user)
            .values_list("created_at", flat=True)
            .distinct(),
        )
    )
    for date in get_dates_for_weeks_count(user, settings.CALENDAR_WEEK_SIZE):
        result.append(
            {"date": date.date(), "is_drunk": bool(date.date() in shot_item_dates)}
        )
    return result
