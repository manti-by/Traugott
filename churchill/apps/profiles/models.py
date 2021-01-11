from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from churchill.apps.core.models import BaseModel


class Profile(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
    )
    image = models.FileField(upload_to=settings.PROFILE_IMAGE_DIRECTORY)

    language = models.CharField(max_length=5, choices=settings.LANGUAGES)
    currency = models.ForeignKey(
        "currencies.Currency", related_name="profiles", on_delete=models.DO_NOTHING
    )

    avg_consumption = models.IntegerField(
        default=settings.AVG_ALCOHOL_CONSUMPTION,
        help_text=_("Average alcohol consumption in ml per year"),
    )
    avg_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=settings.AVG_ALCOHOL_PRICE,
        help_text=_("Average alcohol price for 1000 ml"),
    )

    def __str__(self):
        return self.user.email
