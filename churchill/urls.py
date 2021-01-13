from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="Churchill API")


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("api/", include("churchill.api.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
