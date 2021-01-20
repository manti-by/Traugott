from datetime import timedelta
from decimal import Decimal
from typing import Optional

from django.utils import timezone

from churchill.apps.profiles.models import Profile
from churchill.apps.shots.models import ShotItem


def update_profile(
    profile: Profile,
    language: Optional[str] = None,
    currency: Optional[str] = None,
    avg_consumption: Optional[int] = None,
    avg_price: Optional[Decimal] = None,
) -> Profile:
    if language is not None:
        profile.language = language

    if currency is not None:
        profile.currency = currency

    if avg_consumption is not None:
        profile.avg_consumption = avg_consumption

    if avg_price is not None:
        profile.avg_price = avg_price

    profile.save()
    return profile


def get_profile_stats(profile: Profile) -> Optional[dict]:
    last_shot = ShotItem.objects.filter(user=profile.user).order_by("created_at").last()
    if last_shot:
        volume, money = calculate_skipped_stats(last_shot)
        return {
            "last_shot_at": last_shot.created_at,
            "timedelta_last_shot": timezone.now() - last_shot.created_at,
            "skipped_volume_last_shot": volume,
            "money_saved_last_shot": money,
        }


def calculate_skipped_stats(last_shot: ShotItem) -> tuple:
    volume = 0
    money = 0
    return volume, money
