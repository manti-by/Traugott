from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from churchill.apps.core.models import BaseModel


class ShotManager(models.Manager):

    def for_user(self, user: User):
        return self.filter(
            Q(created_by=user) | Q(is_public=True, is_approved=True)
        )


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

    objects = ShotManager()

    def __str__(self):
        return self.title


class ShotItem(BaseModel):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shot_items",
    )
    shot = models.ForeignKey(
        Shot,
        on_delete=models.CASCADE,
        related_name="items",
    )

    def __str__(self):
        return f"{self.user} - {self.shot}"
