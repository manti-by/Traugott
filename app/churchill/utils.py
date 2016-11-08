import random

from datetime import tzinfo, timedelta
from os.path import splitext


def _unique():
    return str(''.join([str(random.randint(0, 9)) for _ in range(16)]))


def get_name(instance, filename, type):
    name, ext = splitext(filename)
    return instance.__class__.__name__.lower() + '/' + type + '/' + _unique() + ext


def image_name(instance, filename):
    return get_name(instance, filename, 'image')


def preview_name(instance, filename):
    return get_name(instance, filename, 'preview')


def thumb_name(instance, filename):
    return get_name(instance, filename, 'thumb')


ZERO = timedelta(0)

class UTC(tzinfo):
    def utcoffset(self, dt):
        return ZERO
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return ZERO

utc = UTC()
