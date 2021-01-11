from django.db import models
from django.utils.translation import gettext_lazy as _

from churchill.apps.core.models import BaseModel


class Currency(BaseModel):
    name = models.CharField(max_length=32)
    iso3 = models.CharField(max_length=3)
    sign = models.CharField(max_length=1, null=True, blank=True)

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return self.name


class CurrencyValueType(models.TextChoices):
    BUY = "BUY", _("Buy")
    SELL = "SELL", _("Sell")


class CurrencyValue(BaseModel):
    currency = models.ForeignKey(
        "currencies.Currency", related_name="values", on_delete=models.CASCADE
    )
    type = models.CharField(max_length=4, choices=CurrencyValueType.choices)
    value = models.DecimalField(max_digits=7, decimal_places=4)

    class Meta:
        verbose_name = _("Currency Value")
        verbose_name_plural = _("Currency Values")

    def __str__(self):
        return f"{self.currency.name} at {self.created_at}"
