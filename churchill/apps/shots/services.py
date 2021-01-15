from decimal import Decimal
from typing import Optional

from django.contrib.auth.models import User

from churchill.apps.shots.models import Shot


def create_shot(
    user: User, title: str, volume: int, degree: int, cost: Optional[Decimal] = 0.0
) -> Shot:
    return Shot.objects.create(
        title=title, volume=volume, degree=degree, cost=cost, created_by=user
    )


def delete_shot(user: User, id_list: list):
    Shot.objects.filter(id__in=id_list, created_by=user).delete()
