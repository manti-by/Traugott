import json

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.template import Library

register = Library()


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return json.dumps(object, default=date_handler)

register.filter('jsonify', jsonify)