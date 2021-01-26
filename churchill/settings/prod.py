from .base import *  # noqa

DEBUG = False

SECRET_KEY = "sa$j2w22j^1o1q)a0wcrg8ghv%$kf^vedb+6utq18yr%3#6se9"

ALLOWED_HOSTS = ["127.0.0.1", "churchill.manti.by"]

BASE_URL = "https://churchill.manti.by"

STATIC_ROOT = "/srv/churchill/static/"
MEDIA_ROOT = "/srv/churchill/media/"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/srv/churchill/data/db.sqlite3",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "churchill",
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "app": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "/var/log/churchill/app.log",
        },
        "django": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "/var/log/churchill/django.log",
        },
        "console": {"level": "DEBUG", "class": "logging.StreamHandler"},
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "": {
            "handlers": ["app"],
            "level": "WARNING",
            "propagate": True,
            "formatter": "verbose",
        },
        "django": {
            "handlers": ["django"],
            "level": "WARNING",
            "propagate": True,
            "formatter": "simple",
        },
        "django.template": {"handlers": ["null"]},
        "django.db.backends": {"handlers": ["null"]},
    },
}
