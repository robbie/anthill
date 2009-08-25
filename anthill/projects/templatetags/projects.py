import datetime
from django import template
from django.db.models import Count
from anthill.utils import get_items_as_tag, chart_from_tags, _extract_chart_params, ChartNode
from anthill.projects.models import Project
from newsfeed.models import FeedItem

register = template.Library()

@register.tag
def get_active_projects(parser, token):
    start_time = datetime.datetime.now() - datetime.timedelta(30)  # month ago
    most_active = FeedItem.objects.filter(timestamp__gt=start_time).values_list('feed__slug', flat=True).order_by('count').annotate(count=Count('id'))[:5]
    projects = Project.objects.filter(slug__in=list(most_active))
    if hasattr(projects, '_gatekeeper'):
        projects = projects.approved()
    return get_items_as_tag(token, projects)

@register.tag
def project_skills_piechart(parser, token):
    return chart_from_tags(Project, token)

@register.tag
def project_official_piechart(parser, token):
    width, height, args = _extract_chart_params(token)
    args = [arg.split(':') for arg in args]
    items = Project.objects.values('official').annotate(num=Count('id'))
    for item in items:
        if item.pop('official'):
            item['name'] = args[0][0]
            item['color'] = args[0][1]
        else:
            item['name'] = args[1][0]
            item['color'] = args[1][1]
    return ChartNode(items, width, height, chart_type='bhs')
