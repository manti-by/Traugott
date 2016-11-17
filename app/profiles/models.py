from django.db import models
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static

from churchill.mixins import ImageMixin


class Profile(ImageMixin, models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profiles',
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    def as_dict(self):
        if self.image:
            image_url = self.image.url
        else:
            image_url = static('img/user.png')
        return {'id': self.user.id, 'email': self.user.email, 'image': image_url}

    @staticmethod
    def get_logged(request):
        if not request.user.is_authenticated:
            return None
        try:
            user = User.objects.get(id=request.user.id)
            if not user.profiles:
                profile = Profile(user=user)
                profile.save()
            return user.profiles
        except Exception as e:
            pass
        return None

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
            return user.profiles
        return None
