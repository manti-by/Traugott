from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("user/", include("rest_auth.urls")),
    path("user/signup/", include("rest_auth.urls")),
    path("v1/", include("churchill.api.v1.urls", namespace="v1")),
]
