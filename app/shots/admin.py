from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.templatetags.staticfiles import static as static_file

from shots.models import ShotIcon, ShotType, Shot
from churchill.mixins import IMAGES_HELP_TEXT


@admin.register(ShotIcon)
class ShotIconAdmin(admin.ModelAdmin):

    list_display = ('icon_image', 'title')
    ordering = ('title',)

    fieldsets = (
        (_('Info'), {
            'fields': ('title',)
        }),
        (_('Images'), {
            'fields': ('image', 'thumb', 'preview'),
            'description': '<div class="help">%s</div>' % IMAGES_HELP_TEXT,
        }),
    )

    def icon_image(self, obj):
        icon = static_file('img/no-image.png')
        if obj.thumb:
            icon = obj.thumb.url
        return mark_safe('<img src="%s" width="50" />' % icon)
    icon_image.short_description = _('Icon')


@admin.register(ShotType)
class ShotTypeAdmin(admin.ModelAdmin):

    list_display = ('icon_image', 'title', 'volume', 'measure', 'degree')
    ordering = ('title',)

    fieldsets = (
        (_('Info'), {
            'fields': ('title', ('volume', 'measure'), 'degree')
        }),
        (_('Externals'), {
            'fields': ('icon', 'user', 'is_public')
        }),
    )

    def icon_image(self, obj):
        icon = static_file('img/no-image.png')
        if obj.icon and obj.icon.thumb:
            icon = obj.icon.thumb.url
        return mark_safe('<img src="%s" width="50" />' % icon)
    icon_image.short_description = _('Icon')


@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):

    list_display = ('icon_image', 'created', 'user', 'title', 'volume', 'measure', 'degree')
    ordering = ('created',)

    def icon_image(self, obj):
        icon = static_file('img/no-image.png')
        if obj.type.icon and obj.type.icon.thumb:
            icon = obj.type.icon.thumb.url
        return mark_safe('<img src="%s" width="50" />' % icon)
    icon_image.short_description = _('Icon')

    def title(self, obj):
        return obj.type.title

    def volume(self, obj):
        return obj.type.volume

    def measure(self, obj):
        return obj.type.measure

    def degree(self, obj):
        return obj.type.degree
