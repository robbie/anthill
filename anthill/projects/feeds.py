from django.contrib.syndication import feeds
from anthill.projects.models import Project

class ProjectFeed(feeds.Feed):

    title = 'Latest Projects'
    description = 'Latest Projects'
    link = '/projects/all/'

    title_template = 'projects/feed_title.html'
    description_template = 'projects/feed_description.html'

    def items(self):
        return Project.objects.order_by('-creation_date')[:30]

    def item_link(self, item):
        return item.get_absolute_url()

    def item_author_name(self, item):
        return item.lead

    def item_pubdate(self, item):
        return item.creation_date

    def item_categories(self, item):
        return item.tags

