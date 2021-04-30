from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from churchill.apps.core.models import BaseModel
from churchill.apps.currencies.services import get_default_currency_id


class StatsCalculationStrategy(models.TextChoices):
    LAST_SHOT = "LAST_SHOT", _("From the last shot")
    WEEKLY = "WEEKLY", _("Weekly")
    MONTHLY = "MONTHLY", _("Monthly")
    ALL_TIME = "ALL_TIME", _("For the all time")


class Profile(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
    )
    image = models.FileField(
        upload_to=settings.PROFILE_IMAGE_DIRECTORY, null=True, blank=True
    )

    language = models.CharField(
        max_length=5,
        blank=True,
        default=settings.LANGUAGE_CODE,
        choices=settings.LANGUAGES,
    )
    currency = models.ForeignKey(
        "currencies.Currency",
        related_name="profiles",
        on_delete=models.DO_NOTHING,
        blank=True,
        default=get_default_currency_id,
    )
    next_day_offset = models.IntegerField(
        blank=True,
        default=settings.NEXT_DAY_OFFSET,
        help_text=_("Offset in hours for the next day"),
    )

    avg_consumption = models.IntegerField(
        blank=True,
        default=settings.AVG_ALCOHOL_CONSUMPTION,
        help_text=_("Average alcohol consumption in ml per year"),
    )
    avg_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        default=settings.AVG_ALCOHOL_PRICE,
        help_text=_("Average alcohol price for 1000 ml"),
    )
    stats_calculation_strategy = models.CharField(
        max_length=20,
        choices=StatsCalculationStrategy.choices,
        default=StatsCalculationStrategy.MONTHLY,
    )
    verification_token = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.user.email
