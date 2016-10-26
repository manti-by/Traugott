from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9(+8&f)43k--m$cq1#kcwy$%o4hlj9remnlybh+-*gl6_*10*k'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'traugott',
        'USER': 'traugott',
        'PASSWORD': 'pa$$word',
        'HOST': 'localhost',
        'PORT': '',
    }
}



try:
    from .local import *
except ImportError:
    pass
