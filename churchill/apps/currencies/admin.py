from django.contrib import admin

from churchill.apps.currencies.models import Currency, CurrencyValue


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):

    list_display = ("name", "iso3", "created_at")


@admin.register(CurrencyValue)
class CurrencyValueAdmin(admin.ModelAdmin):

    list_display = ("currency", "type", "value", "created_at")
