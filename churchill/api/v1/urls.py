from django.urls import include, path

app_name = "v1"


urlpatterns = [
    path(
        "profile/",
        include("churchill.api.v1.profile.urls"),
        name="profile",
    ),
    path(
        "user/",
        include("churchill.api.v1.user.urls"),
        name="user",
    ),
]
