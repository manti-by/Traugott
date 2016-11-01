from __future__ import unicode_literals

from django.db import models


class ShotType(models.Model):
    title = models.CharField(max_length=10)
    image = models.ImageField(upload_to='shot', blank=True, null=True)
    volume = models.IntegerField(default=100)
    degree = models.IntegerField(default=40)


class Shot(models.Model):
    type = models.OneToOneField(
        ShotType,
        on_delete=models.SET_NULL,
        related_name='shots',
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
