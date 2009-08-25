from django.conf.urls.defaults import *

urlpatterns = patterns('anthill.events.views',
    url(r'^$', 'search', name='event_search'),
    url(r'^(?P<event_id>\d+)/$', 'event_detail', name='event_detail'),
    url(r'^(?P<event_id>\d+)/edit/$', 'edit_event', name='edit_event'),
    url(r'^new/$', 'new_event', name='new_event'),
    url(r'^archive/$', 'archive', name='events_archive'),
    url(r'^archive/(?P<year>\d{4})/$', 'archive_year', name='events_for_year'),
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', name='events_for_month'),
)
