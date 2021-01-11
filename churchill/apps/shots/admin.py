from django.contrib import admin

from churchill.apps.shots.models import Shot


@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):

    list_display = ("title", "volume", "degree", "cost")

    def save_formset(self, request, form, formset, change):
        for f in formset.forms:
            obj = f.instance
            if isinstance(obj, Shot):
                obj.created_by = request.user
            obj.save()
        formset.save()
