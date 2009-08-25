from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic
from tagging.fields import TagField
from markupfield.fields import MarkupField
from brainstorm.models import Idea
from feedinator.models import Subscription

class Project(models.Model):
    slug = models.SlugField('unique identifier for project',
                            max_length=50, unique=True,
                            help_text="(this will become part of your projects URL)")
    name = models.CharField('displayed name of project', max_length=100)
    description = MarkupField(default_markup_type='markdown')
    official = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    tags = TagField('Tags')

    lead = models.ForeignKey(User, related_name='projects_lead_on')
    members = models.ManyToManyField(User, through='Role')
    idea = models.ForeignKey(Idea, blank=True, null=True, related_name='projects')

    subscriptions = generic.GenericRelation(Subscription)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail', args=[self.slug])

    def get_members(self):
        return self.members.filter(project_roles__status='A')

ROLE_STATUSES = (
    ('P', 'Pending'),
    ('A', 'Active'),
    ('R', 'Retired')
)

class Role(models.Model):
    user = models.ForeignKey(User, related_name='project_roles')
    project = models.ForeignKey(Project, related_name='roles')
    join_time = models.DateField(auto_now_add=True)
    status = models.CharField(choices=ROLE_STATUSES, max_length=1, default='P')
    message = models.TextField(blank=True)

SITE_LINK, SOURCE_LINK, DOCS_LINK, DOWNLOAD_LINK, EMAIL_LINK = range(5)
LINK_TYPES = (
    (SITE_LINK, 'website'),
    (SOURCE_LINK, 'source'),
    (DOCS_LINK, 'documentation'),
    (DOWNLOAD_LINK, 'download'),
    (EMAIL_LINK, 'email'),
)

class Link(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    link_type = models.PositiveSmallIntegerField(choices=LINK_TYPES)

    project = models.ForeignKey(Project, related_name='links')

    class Meta:
        ordering = ['link_type']

class Ask(models.Model):
    message = models.CharField(max_length=200)
    project = models.ForeignKey(Project, related_name='asks')
    user = models.ForeignKey(User, related_name='asks')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return self.message
