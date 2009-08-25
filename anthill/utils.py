from django import template
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from tagging.models import Tag

class SimpleItemsNode(template.Node):
    def __init__(self, queryset, count, offset, varname):
        self.items = queryset[offset:count+offset]
        self.varname = varname

    def render(self, context):
        context[self.varname] = self.items
        return ''

def get_items_as_tag(token, queryset, count=5):
    pieces = token.contents.split()
    as_index = pieces.index('as')
    if as_index == -1 or as_index > 3 or len(pieces) != as_index+2:
        raise template.TemplateSyntaxError('%r tag must be in format {%% %r [count [offset]] as varname %%}' %
                                          pieces[0])

    # count & offset
    offset = 0
    if as_index > 1:
        count = int(pieces[1])
        if as_index > 2:
            count = int(pieces[2])

    varname = pieces[as_index+1]

    return SimpleItemsNode(queryset, count, offset, varname)


## google charts ##

class ChartNode(template.Node):
    def __init__(self, items, width=150, height=150, chart_type='bhs'):
        nums = []
        snums = []
        names = []
        colors = []
        for item in items:
            nums.append(item['num'])
            snums.append(str(item['num']))
            names.append(item['name'])
            colors.append(item['color'])

        chart_data = {'width': width, 'height': height, 'nums':','.join(snums),
                      'names':'|'.join(names), 'colors':'|'.join(colors),
                      'scale': max(nums)+5, 'chart_type':chart_type}
        self.img_url = 'http://chart.apis.google.com/chart?cht=%(chart_type)s&chds=0,%(scale)s&chdlp=b&chf=bg,s,00000000&chd=t:%(nums)s&chs=%(width)dx%(height)d&chdl=%(names)s&chco=%(colors)s' % chart_data

    def render(self, context):
        return '<img src="%s" />' % self.img_url

def _extract_chart_params(token, width=150, height=150):
    pieces = token.contents.split()
    args = pieces[1:]
    if ':' not in args[0] and 'x' in args[0]:
        width, height = args[0].split('x')
        width = int(width)
        height = int(height)
        args = args[1:]
    return width, height, args

def chart_from_tags(model, token):
    width, height, args = _extract_chart_params(token)
    tags = dict(arg.split(':') for arg in args)
    ct = ContentType.objects.get_for_model(model).id
    tag_names = tags.keys()
    items = Tag.objects.filter(items__content_type=ct, name__in=tag_names).values('name').annotate(num=Count('id'))
    for item in items:
        item['color'] = tags[item['name']]
    return ChartNode(items, width, height, chart_type='bhs')

