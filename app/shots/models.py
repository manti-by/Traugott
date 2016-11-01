from __future__ import unicode_literals

from django.db import models

from traugott.mixins import ImageMixin


class ShotType(ImageMixin, models.Model):
    title = models.CharField(max_length=100)
    volume = models.IntegerField(default=100)
    degree = models.IntegerField(default=40)

    def __str__(self):
        return self.title


class Shot(models.Model):
    type = models.OneToOneField(
        ShotType,
        on_delete=models.SET_NULL,
        related_name='shots',
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.created.strftime('%d/%m %H:%M'), self.type.title)

