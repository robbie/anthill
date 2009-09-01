import datetime
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

MESSAGE_WAIT_PERIOD = 2
INITIAL_MAX_MESSAGES = 100

class Profile(LocationModel):
    user = models.OneToOneField(User, related_name='profile')
    url = models.URLField(blank=True)
    about = MarkupField(blank=True, default_markup_type=settings.ANTHILL_DEFAULT_MARKUP)
    role = models.CharField(max_length=5, choices=ROLES, default='other')
    twitter_id = models.CharField(max_length=15, blank=True)
    skills = TagField('comma separated list of your skills (eg. python, django)')

    # other metadata
    allow_org_emails = models.BooleanField(default=False)
    signup_date = models.DateTimeField(auto_now_add=True)
    last_email_sent = models.DateTimeField(null=True)
    num_emails_sent = models.IntegerField(default=0)
    allowed_emails = models.IntegerField(default=INITIAL_MAX_MESSAGES)

    def __unicode__(self):
        return unicode(self.user)

    def can_send_email(self):
        if self.last_email_sent:
            elapsed = datetime.datetime.now() - self.last_email_sent
        else:
            elapsed = datetime.timedelta(minutes=MESSAGE_WAIT_PERIOD+1)
        return (elapsed > datetime.timedelta(minutes=MESSAGE_WAIT_PERIOD) and
                self.num_emails_sent < self.allowed_emails)

    def record_email_sent(self):
        self.last_email_sent = datetime.datetime.now()
        self.num_emails_sent += 1
        self.save()

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(create_profile, sender=User)
