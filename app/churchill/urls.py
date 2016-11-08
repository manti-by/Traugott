from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from churchill.views import home_page, static_page
from profiles.views import login_page, logout_page
from shots.views import shots_add, shots_update, shots_delete


urlpatterns = [
    url(r'^$', home_page, name='index'),
    url(r'^about$', static_page, {'page': 'about'}, name='about'),

    # Profile urls
    url(r'^profiles/login/?$', login_page, name='login'),
    url(r'^profiles/logout/?$', logout_page, name='logout'),

    # Shot urls
    url(r'^shots/add/?$', shots_add, name='shots_add'),
    url(r'^shots/update/?$', shots_update, name='shots_update'),
    url(r'^shots/delete/?$', shots_delete, name='shots_delete'),

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
