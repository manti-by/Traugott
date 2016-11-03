from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static as static_file

from traugott.mixins import ImageMixin


class ShotTypeManager(models.Manager):

    def get_for_user(self, user):
        return super(ShotTypeManager, self).get_queryset().filter(shots__user=user)


class ShotType(ImageMixin, models.Model):

    title = models.CharField(max_length=100)
    volume = models.IntegerField(default=100)
    degree = models.IntegerField(default=40)
    objects = ShotTypeManager()

    def __str__(self):
        return self.title

    def as_dict(self):
        if self.thumb:
            image_url = self.thumb.url
        elif self.image:
            image_url = self.image.url
        else:
            image_url = static_file('img/no-image.png')
        return {'title': self.title, 'image': image_url,
                'volume': self.volume, 'degree': self.degree}


class Shot(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shots',
        null=True,
    )
    type = models.OneToOneField(
        ShotType,
        on_delete=models.SET_NULL,
        related_name='shots',
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.created.strftime('%d/%m %H:%M'), self.type.title)

    def as_dict(self):
        if self.type.image:
            image_url = self.type.image.url
        else:
            image_url = static_file('img/no-image.png')
        return {'date': self.created.strftime('%d/%m %H:%M'), 'image': image_url,
                'text': '%s, %sml' % (self.type.title, self.type.volume)}
