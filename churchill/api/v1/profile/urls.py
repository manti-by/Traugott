from django.urls import path

from churchill.api.v1.profile.views import ProfileView, ProfileImageView

app_name = "profile"


urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("image/", ProfileImageView.as_view(), name="profile_image"),
]
