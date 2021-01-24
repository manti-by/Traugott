from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, Tuple

from django.utils import timezone

from churchill.apps.profiles.exception import InvalidStatsCalculationStrategyException
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
        volume, money = calculate_consuming_stats(profile, last_shot)
        timedelta_last_shot = timezone.now() - last_shot.created_at
        return {
            "last_shot_at": last_shot.created_at,
            "timedelta_last_shot": timedelta_last_shot,
            "timedelta_last_shot_repr": str(timedelta_last_shot).split(".")[0],
            "skipped_volume_last_shot": volume,
            "money_saved_last_shot": money,
        }


def get_drunk_and_all_days_count(profile: Profile, from_date: datetime) -> Tuple[int, int]:
    drunk_days = profile.user.shot_items.filter(created_at__gte=from_date).count()
    all_days = int((timezone.now() - from_date).days)
    return drunk_days, all_days


def get_last_shot_stats(profile: Profile, last_shot: ShotItem) -> Tuple[int, int]:
    return get_drunk_and_all_days_count(profile, last_shot.created_at)


def get_weekly_stats(profile: Profile, *args) -> Tuple[int, int]:
    return get_drunk_and_all_days_count(profile, timezone.now() - timedelta(days=7))


def get_monthly_stats(profile: Profile, *args) -> Tuple[int, int]:
    return get_drunk_and_all_days_count(profile, timezone.now() - timedelta(days=30))


def get_all_time_stats(profile: Profile, *args) -> Tuple[int, int]:
    return get_drunk_and_all_days_count(profile, profile.created_at)


def calculate_consuming_stats(profile: Profile, last_shot: ShotItem) -> Tuple[int, Decimal]:
    switcher = {
        "LAST_SHOT": get_last_shot_stats,
        "WEEKLY": get_weekly_stats,
        "MONTHLY": get_monthly_stats,
        "ALL_TIME": get_all_time_stats,
    }
    func = switcher.get(profile.stats_calculation_strategy)
    if func is None:
        raise InvalidStatsCalculationStrategyException
    drunk_days, all_days = func(profile, last_shot)
    skipped_volume = Decimal((all_days - drunk_days) * profile.avg_consumption / 365)
    skipped_money = round(skipped_volume * profile.avg_price / 1000, 2)
    return int(skipped_volume), Decimal(skipped_money)
