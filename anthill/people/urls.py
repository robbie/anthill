from django.conf.urls.defaults import *

urlpatterns = patterns('anthill.people.views',
    url(r'^$', 'search', name='user_search'),
    url(r'^edit_profile/$', 'edit_profile', name='edit_profile'),
    url(r'^change_password/$', 'change_password', name='change_password'),
    url(r'^(?P<username>\w+)/$', 'profile', name='user_profile'),
    url(r'^(?P<username>\w+)/contact/$', 'contact', name='contact_user'),
)
