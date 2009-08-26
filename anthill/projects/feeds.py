from django.contrib.syndication import feeds
from anthill.projects.models import Project, Ask

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


class AskFeed(feeds.Feed):

    title = 'Latest Asks'
    description = 'Latest requests for help from all projects'
    link = '/projects/asks/'

    title_template = 'projects/ask_feed_title.html'
    description_template = 'projects/ask_feed_description.html'

    def items(self):
        return Ask.objects.select_related()

    def item_link(self, item):
        return item.project.get_absolute_url()

    def item_author_name(self, item):
        return item.user

    def item_pubdate(self, item):
        return item.timestamp
