from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from tagging.fields import TagField
from markupfield.fields import MarkupField
from anthill.models import LocationModel

ROLES = (
    ('other', 'Community Member'),
    ('des', 'Designer'),
    ('dev', 'Developer'),
    ('both', 'Developer/Designer'),
)

class Profile(LocationModel):
    user = models.OneToOneField(User, related_name='profile')
    url = models.URLField(blank=True)
    about = MarkupField(blank=True, default_markup_type=settings.ANTHILL_DEFAULT_MARKUP)
    role = models.CharField(max_length=5, choices=ROLES, default='other')
    twitter_id = models.CharField(max_length=15, blank=True)
    skills = TagField('comma separated list of your skills (eg. python, django)')

    allow_org_emails = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.user)

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(create_profile, sender=User)
