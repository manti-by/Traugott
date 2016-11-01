from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.translation import ugettext_lazy as _

from traugott.utils import image_name, preview_name, thumb_name
from sorl.thumbnail import get_thumbnail


IMAGES_HELP_TEXT = _('You can select only base image, all others will be generated automatically')

class ImageMixin(models.Model):

    image = models.ImageField(upload_to=image_name, blank=True, null=True, verbose_name=_('Image'))
    thumb = models.ImageField(upload_to=thumb_name, blank=True, null=True, verbose_name=_('Thumbnail'))
    preview = models.ImageField(upload_to=preview_name, blank=True, null=True, verbose_name=_('Preview Image'))

    def save(self, *args, **kwargs):
        super(ImageMixin, self).save(*args, **kwargs)
        if not self.thumb and self.image:
            resized = get_thumbnail(self.image, settings.THUMB_SIZE, crop='center', quality=99)
            self.thumb.save(resized.name, ContentFile(resized.read()), save=True)
            super(ImageMixin, self).save(*args, **kwargs)

        if not self.preview and self.image:
            resized = get_thumbnail(self.image, settings.PREVIEW_SIZE, quality=99)
            self.preview.save(resized.name, ContentFile(resized.read()), save=True)
            super(ImageMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
