from __future__ import absolute_import, unicode_literals

from .base import *


DEBUG = True

SECRET_KEY = '9(+8&f)43k--m$cq1#kcwy$%o4hlj9remnlybh+-*gl6_*10*k'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'churchill',
        'USER': 'churchill',
        'PASSWORD': 'pa$$word',
        'HOST': 'localhost',
        'PORT': '',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': [],
            'propagate': False,
            'level':'DEBUG',
        },
    },
}

CACHES = {
    'default': {

    }
}

USE_COMPRESSOR = False

try:
    from .local import *
except ImportError:
    pass
