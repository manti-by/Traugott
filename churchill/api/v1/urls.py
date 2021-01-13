from django.urls import include, path

app_name = "v1"


urlpatterns = [
    path(
        "profiles/",
        include("churchill.api.v1.profiles.urls"),
        name="profiles",
    )
]
