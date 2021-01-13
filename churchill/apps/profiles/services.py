from decimal import Decimal
from typing import Optional

from churchill.apps.profiles.models import Profile


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
