from django.contrib import admin

from shots.models import ShotType, Shot


@admin.register(ShotType)
class ShotTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):
    pass
