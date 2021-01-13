from django.urls import path

from churchill.api.v1.profiles.views import ProfilesView, ProfilesImageView

app_name = "profiles"


urlpatterns = [
    path("", ProfilesView.as_view(), name="profile"),
    path("image/", ProfilesImageView.as_view(), name="profile_image"),
]
