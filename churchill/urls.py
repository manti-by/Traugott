from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView

from churchill.apps.core.views import verify_email

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("worker.js", TemplateView.as_view(template_name="worker.js"), name="worker"),
    path("verify-email/", verify_email, name="verify_email"),
    path("api/", include("churchill.api.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
