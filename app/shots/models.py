from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static as static_file

from churchill.mixins import ImageMixin
from churchill.utils import utc


class ShotTypeManager(models.Manager):

    def get_for_user(self, user):
        return super(ShotTypeManager, self).get_queryset() \
            .filter(shots__user=user, shots__deleted=0).distinct()

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
        return {'id': self.id, 'title': self.title, 'image': image_url,
                'volume': self.volume, 'degree': self.degree}


class ShotManager(models.Manager):

    def get_for_user(self, user):
        return super(ShotManager, self).get_queryset().filter(user=user, deleted=0)

    def get_for_response(self, user):
        result = []
        for item in self.get_for_user(user).order_by('-created'):
            result.append(item.as_dict())
        return result


class Shot(models.Model):

    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='shots',
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
        if self.type.image:
            image_url = self.type.image.url
        else:
            image_url = static_file('img/no-image.png')

        if self.type.thumb:
            thumb_url = self.type.thumb.url
        else:
            thumb_url = static_file('img/no-image.png')

        if self.quantity > 1:
            text = '%s, %d&times;%sml' % (self.type.title, self.quantity, self.type.volume)
        else:
            text = '%s, %sml' % (self.type.title, self.type.volume)
        return {'id': self.id, 'date': self.human_date, 'text': text, 'quantity': self.quantity,
                'image': image_url, 'thumb': thumb_url, 'type': self.type.as_dict()}
