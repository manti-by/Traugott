import json

from django import template

from churchill import VERSION

register = template.Library()


@register.simple_tag
def app_version():
    return VERSION


@register.filter
def messages_to_json(messages):
    return json.dumps([{"level": m.level_tag, "message": m.message} for m in messages])
