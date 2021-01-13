from decimal import Decimal
from typing import Optional

from django.contrib.auth.models import User

from churchill.apps.profiles.models import Profile


def update_profile(
    user: User,
    language: Optional[str] = None,
    currency: Optional[str] = None,
    avg_consumption: Optional[int] = None,
    avg_price: Optional[Decimal] = None,
) -> Profile:
    if language is not None:
        user.profile.language = language

    if currency is not None:
        user.profile.currency = currency

    if avg_consumption is not None:
        user.profile.avg_consumption = avg_consumption

    if avg_price is not None:
        user.profile.avg_price = avg_price

    user.profile.save()

    return user.profile
