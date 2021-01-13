from django.urls import path

from churchill.api.v1.profiles.views import ProfilesView

app_name = "profiles"


urlpatterns = [
    path(
        "",
        ProfilesView.as_view(),
        name="profiles",
    ),
]
