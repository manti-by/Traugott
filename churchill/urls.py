from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from churchill.apps.core.views import index_view, verify_email

urlpatterns = [
    path("", index_view, name="index"),
    path("verify-email/", verify_email, name="verify_email"),
    path("api/", include("churchill.api.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
