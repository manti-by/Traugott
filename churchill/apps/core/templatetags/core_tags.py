import json

from django import template

register = template.Library()


@register.filter(name="messages_to_json")
def messages_to_json(messages):
    return json.dumps([{"level": m.level_tag, "message": m.message} for m in messages])
