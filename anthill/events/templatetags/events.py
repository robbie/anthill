from django import template
from anthill.utils import get_items_as_tag
from anthill.events.models import Event

register = template.Library()

@register.tag
def get_official_events(parser, token):
    return get_items_as_tag(token, Event.objects.future().filter(official=True))

@register.tag
def get_upcoming_events(parser, token):
    return get_items_as_tag(token, Event.objects.future())
