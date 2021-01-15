from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from churchill.apps.core.models import BaseModel


class Shot(BaseModel):

    title = models.CharField(max_length=100)
    volume = models.IntegerField(default=100, help_text=_("Volume in ml"))
    degree = models.IntegerField(default=40, help_text=_("The strength of alcohol"))
    cost = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)

    is_public = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="shots",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title
