import json

from django import template
from django.utils.safestring import mark_safe

from churchill import VERSION

register = template.Library()


@register.simple_tag
def app_version():
    return VERSION


@register.filter(is_safe=True)
def jsonify(data):
    return mark_safe(json.dumps(data))


@register.filter(is_safe=True)
def jsonify_messages(messages):
    return mark_safe(
        json.dumps([{"level": m.level_tag, "message": m.message} for m in messages])
    )
