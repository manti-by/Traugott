from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Profile(User):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profiles',
    )
    image = models.ImageField(upload_to='profile', blank=True, null=True)

    def as_dict(self):
        return {'id': self.user.id, 'email': self.user.email, 'image': self.image.url}

    @staticmethod
    def get_or_create(email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(email, email, password)
            user.save()
            profile = Profile(user=user)
            profile.save()
        if user.check_password(password):
            return user
        return None
