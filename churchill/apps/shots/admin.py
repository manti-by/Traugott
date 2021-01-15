from django.contrib import admin

from churchill.apps.shots.models import Shot, ShotItem


@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):

    list_display = ("title", "volume", "degree", "cost", "created_at", "updated_at")

    def save_formset(self, request, form, formset, change):
        for f in formset.forms:
            obj = f.instance
            if isinstance(obj, Shot):
                obj.created_by = request.user
            obj.save()
        formset.save()


@admin.register(ShotItem)
class ShotItemAdmin(admin.ModelAdmin):

    list_display = ("user", "shot", "created_at", "updated_at")
    raw_id_fields = ("user", "shot")
