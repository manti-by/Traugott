from django.urls import path

from churchill.api.v1.shots.views import ShotsView, ShotsItemView

app_name = "shots"


urlpatterns = [
    path("", ShotsView.as_view(), name="shots"),
    path("item/", ShotsItemView.as_view(), name="item"),
]
