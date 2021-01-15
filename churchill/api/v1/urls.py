from django.urls import include, path

app_name = "v1"


urlpatterns = [
    path(
        "profile/",
        include("churchill.api.v1.profile.urls"),
        name="profile",
    ),
    path(
        "shots/",
        include("churchill.api.v1.shots.urls"),
        name="shots",
    ),
    path(
        "user/",
        include("churchill.api.v1.user.urls"),
        name="user",
    ),
]
