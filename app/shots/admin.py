from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.templatetags.staticfiles import static as static_file

from shots.models import ShotType, Shot
from traugott.mixins import IMAGES_HELP_TEXT


@admin.register(ShotType)
class ShotTypeAdmin(admin.ModelAdmin):

    list_display = ('thumb_image', 'title', 'volume', 'degree')
    ordering = ('title',)

    fieldsets = (
        (_('Info'), {
            'fields': ('title', 'volume', 'degree')
        }),
        (_('Images'), {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('image', 'thumb', 'preview'),
            'description': '<div class="help">%s</div>' % IMAGES_HELP_TEXT,
        })
    )

    def thumb_image(self, obj):
        image = static_file('img/no-image.png')
        if obj.thumb:
            image = obj.thumb.url
        return mark_safe('<img src="%s" width="50" />' % image)
    thumb_image.short_description = _('Image')


@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):

    list_display = ('thumb_image', 'created', 'title', 'volume', 'degree')
    ordering = ('created',)

    def thumb_image(self, obj):
        image = static_file('img/no-image.png')
        if obj.type.thumb:
            image = obj.type.thumb.url
        return mark_safe('<img src="%s" width="50" />' % image)
    thumb_image.short_description = _('Image')

    def title(self, obj):
        return obj.type.title

    def volume(self, obj):
        return obj.type.volume

    def degree(self, obj):
        return obj.type.degree
