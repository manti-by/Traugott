import random

from os.path import splitext
from datetime import datetime, timedelta


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


def random_date():
    start = datetime.strptime('9/9/2016 1:30 PM', '%m/%d/%Y %I:%M %p')
    end = datetime.strptime('10/10/2016 4:50 AM', '%m/%d/%Y %I:%M %p')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)
