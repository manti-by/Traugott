from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from traugott.views import index
from profiles.views import ProfileResource


urlpatterns = [
    url(r'^$', index, name='index'),

    # Profile urls
    url(r'^profiles/?$', ProfileResource.as_view()),
    url(r'^profiles/(?P<id>[0-9]+)/?$', ProfileResource.as_view()),

    # Admin urls
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
