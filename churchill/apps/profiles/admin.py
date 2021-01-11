from django.contrib import admin

from churchill.apps.profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ("user", "language", "currency", "created_at")
