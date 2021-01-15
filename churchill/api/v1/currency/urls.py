from django.urls import path

from churchill.api.v1.currency.views import CurrencyView

app_name = "currency"


urlpatterns = [
    path("", CurrencyView.as_view(), name="currency"),
]
