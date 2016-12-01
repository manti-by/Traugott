from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static as static_file

from churchill.mixins import ImageMixin
from churchill.utils import utc


MEASURE_CHOICES = (
    ('ml', 'Milliliter'),
    ('gr', 'Grams'),
    ('pc', 'Piece'),
)

VOLUME_CHOICES = (
    ('ml', (50, 100, 200, 330, 500, 750)),
    ('gr', (0.5, 1, 2, 3, 5, 10, 20)),
    ('pc', (1, 2, 3, 4, 5, 10, 20)),
)


class ShotIconManager(models.Manager):

    def get_for_response(self, user):
        result = []
        for icon in super(ShotIconManager, self).get_queryset().all():
            result.append(icon.as_dict())
        return result


class ShotIcon(ImageMixin, models.Model):

    title = models.CharField(max_length=100)
    objects = ShotIconManager()

    def __str__(self):
        return self.title

    def as_dict(self):
        image_url = thumb_url = static_file('img/no-image.png')
        if self.image:
            image_url = self.image.url
        if self.thumb:
            thumb_url = self.thumb.url
        return {'id': self.id, 'title': self.title, 'image': image_url, 'thumb': thumb_url  }


class ShotTypeManager(models.Manager):

    def get_for_user(self, user):
        return super(ShotTypeManager, self).get_queryset() \
            .filter(deleted=0, shots__user=user, shots__deleted=0).distinct()

    def get_for_response(self, user):
        result = []
        for item in self.get_for_user(user):
            result.append(item.as_dict())
        return result

    def get_splitted_for_user(self, user):
        user_shot_types = []
        user_shot_types_ids = []
        for shot_type in self.get_for_user(user):
            user_shot_types.append(shot_type.as_dict())
            user_shot_types_ids.append(shot_type.id)

        all_shot_types = []
        for shot_type in super(ShotTypeManager, self).get_queryset() \
                .exclude(id__in=user_shot_types_ids):
            all_shot_types.append(shot_type.as_dict())

        return user_shot_types, all_shot_types


class ShotType(models.Model):

    title = models.CharField(max_length=100)
    measure = models.CharField(max_length=2, choices=MEASURE_CHOICES, default='ml')
    volume = models.IntegerField(default=100, help_text='')
    degree = models.IntegerField(default=40, help_text='Alcohol percentage or "strength"')
    cost = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='shot_types',
        default=settings.DEFAULT_ADMIN_USER_ID,
        null=True,
    )
    icon = models.ForeignKey(
        ShotIcon,
        on_delete=models.SET_NULL,
        related_name='shot_types',
        null=True,
    )
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.IntegerField(default=0)
    objects = ShotTypeManager()

    def __str__(self):
        return self.title

    def as_dict(self):
        image_url = thumb_url = static_file('img/no-image.png')
        if self.icon:
            if self.icon.image:
                image_url = self.icon.image.url
            if self.icon.thumb:
                thumb_url = self.icon.thumb.url
        return {'id': self.id, 'title': self.title, 'image': image_url, 'thumb': thumb_url,
                'volume': self.volume, 'degree': self.degree, 'measure': self.measure }


class ShotManager(models.Manager):

    def get_for_user(self, user):
        return super(ShotManager, self).get_queryset() \
            .filter(user=user, deleted=0, type__deleted=0)

    def get_for_response(self, user):
        result = []
        for item in self.get_for_user(user).order_by('-created'):
            result.append(item.as_dict())
        return result


class Shot(models.Model):

    volume = models.IntegerField(default=0)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='shots',
        default=settings.DEFAULT_ADMIN_USER_ID,
        null=True,
    )
    type = models.ForeignKey(
        ShotType,
        on_delete=models.SET_NULL,
        related_name='shots',
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.IntegerField(default=0)
    objects = ShotManager()

    @property
    def human_date(self):
        delta = datetime.now(utc) - self.created
        if delta.total_seconds() < 60 * 60:
            return 'just now'
        elif delta.total_seconds() < 60 * 60 * 5:
            return '%sh ago' % str(int(delta.total_seconds() / (60 * 60)))
        elif delta.total_seconds() < 60 * 60 * 24:
            return 'today'
        elif delta.total_seconds() < 60 * 60 * 24 * 7:
            return '%sd ago' % str(int(delta.total_seconds() / (60 * 60 * 24)))
        else:
            return self.created.strftime('%b %d')

    def __str__(self):
        return '%s %s' % (self.created.strftime('%b %d'), self.type.title)

    def as_dict(self):
        image_url = thumb_url = static_file('img/no-image.png')
        if self.type and self.type.icon:
            if self.type.icon.image:
                image_url = self.type.icon.image.url
            if self.type.icon.thumb:
                thumb_url = self.type.icon.thumb.url
        text = '%s, %d&times;%sml' % (self.type.title, (self.volume / self.type.volume), self.type.volume)
        return {'id': self.id, 'date': self.human_date, 'text': text,
                'volume': self.volume, 'step': self.type.volume,
                'image': image_url, 'thumb': thumb_url, 'type': self.type.as_dict()}

