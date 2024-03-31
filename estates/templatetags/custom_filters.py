from django import template
from urllib.parse import urlencode

register = template.Library()

@register.filter
def getattr_filter(obj, attr):
    try:
        return getattr(obj, attr)
    except AttributeError:
        return None

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)