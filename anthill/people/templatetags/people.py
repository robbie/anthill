from django import template
from django.conf import settings
from django.db.models import Count
from anthill.utils import get_items_as_tag, chart_from_tags, _extract_chart_params, ChartNode
from anthill.people.models import Profile

register = template.Library()

@register.tag
def get_latest_user_profiles(parser, token):
    return get_items_as_tag(token,
         Profile.objects.all().select_related().order_by('-user__date_joined'))

@register.simple_tag
def display_name(user):
    return user.first_name or user.username

@register.simple_tag
def possessive(user):
    name = user.first_name or user.username
    if name[-1] == 's':
        name = ''.join((name, "'"))
    else:
        name = ''.join((name, "'s"))
    return name

@register.simple_tag
def num_registered_users():
    return Profile.objects.all().count()

@register.simple_tag
def static_google_map(person, width=200, height=200, zoom=12):
    base_url = 'http://maps.google.com/staticmap?&sensor=false&key=%(key)s&markers=%(lat)s,%(long)s&zoom=%(zoom)s&size=%(width)sx%(height)s'
    return base_url % {'lat':person.lat_long.x, 'long':person.lat_long.y,
                       'width': width, 'height': height, 'zoom': zoom,
                       'key': settings.GMAPS_API_KEY}

@register.tag
def people_skills_piechart(parser, token):
    return chart_from_tags(Profile, token)

@register.tag
def people_roles_piechart(parser, token):
    width, height, args = _extract_chart_params(token)
    colors = dict(arg.split(':') for arg in args)
    items = Profile.objects.filter(role__in=colors.keys()).values('role').annotate(num=Count('id'))
    for item in items:
        item['name'] = name = item.pop('role')
        item['color'] = colors[name]
    return ChartNode(items, width, height, 'bhs')

