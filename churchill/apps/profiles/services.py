from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, Tuple

from django.db.models import Count
from django.utils import timezone

from churchill.apps.profiles.exception import InvalidStatsCalculationStrategyException
from churchill.apps.profiles.models import Profile
from churchill.apps.shots.models import ShotItem, Shot


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


def get_days_to_balance_count(profile: Profile, volume: int) -> int:
    return int(volume / (profile.avg_consumption / 365) * -1) if volume < 0 else 0


def get_popular_drink_string(profile: Profile, money: Decimal) -> str:
    if money >= 0:
        return ""
    shot = Shot.objects.for_user(profile.user).annotate(items_count=Count("items")).order_by("-items_count").first()
    return f"{round(-1 * money / shot.cost, 1)} shots of {shot.title}"


def get_profile_stats(profile: Profile) -> Optional[dict]:
    last_shot = ShotItem.objects.filter(user=profile.user).order_by("created_at").last()
    if last_shot:
        volume, money = calculate_consuming_stats(profile, last_shot)
        timedelta_last_shot = timezone.now() - last_shot.created_at
        days_to_balance = get_days_to_balance_count(profile, volume)
        popular_drink_string = get_popular_drink_string(profile, money)
        return {
            "last_shot_at": last_shot.created_at,
            "timedelta_last_shot": timedelta_last_shot,
            "timedelta_last_shot_repr": str(timedelta_last_shot).split(".")[0],
            "skipped_volume_last_shot": volume,
            "days_to_balance": days_to_balance,
            "popular_drink": popular_drink_string,
            "money_saved_last_shot": money,
        }


def get_consumption_for_period(
    profile: Profile, from_date: datetime
) -> Tuple[float, float]:
    drunk_days_consumption = 0
    for shot_item in profile.user.shot_items.filter(created_at__gte=from_date):
        drunk_days_consumption += shot_item.spirit_volume
    all_days_consumption = (
        (timezone.now() - from_date).days * profile.avg_consumption / 365
    )
    return drunk_days_consumption, all_days_consumption


def get_last_shot_stats(profile: Profile, last_shot: ShotItem) -> Tuple[float, float]:
    return get_consumption_for_period(profile, last_shot.created_at)


def get_weekly_stats(profile: Profile, *args) -> Tuple[float, float]:
    return get_consumption_for_period(profile, timezone.now() - timedelta(days=7))


def get_monthly_stats(profile: Profile, *args) -> Tuple[float, float]:
    return get_consumption_for_period(profile, timezone.now() - timedelta(days=30))


def get_all_time_stats(profile: Profile, *args) -> Tuple[float, float]:
    return get_consumption_for_period(profile, profile.created_at)


def calculate_consuming_stats(
    profile: Profile, last_shot: ShotItem
) -> Tuple[int, Decimal]:
    switcher = {
        "LAST_SHOT": get_last_shot_stats,
        "WEEKLY": get_weekly_stats,
        "MONTHLY": get_monthly_stats,
        "ALL_TIME": get_all_time_stats,
    }
    func = switcher.get(profile.stats_calculation_strategy)
    if func is None:
        raise InvalidStatsCalculationStrategyException
    drunk_days_consumption, all_days_consumption = func(profile, last_shot)
    skipped_volume = Decimal(all_days_consumption - drunk_days_consumption)
    skipped_money = round(skipped_volume * profile.avg_price / 1000, 2)
    return int(skipped_volume), Decimal(skipped_money)
