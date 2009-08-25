import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.conf import settings
from anthill.models import LocationModel, LocationModelManager
from markupfield.fields import MarkupField

class EventManager(LocationModelManager):
    def future(self):
        now = datetime.datetime.now()
        return self.filter(Q(start_date__gt=now)|Q(end_date__gt=now))


class Event(LocationModel):
    title = models.CharField(max_length=100)
    description = MarkupField(default_markup_type=settings.ANTHILL_DEFAULT_MARKUP)
    official = models.BooleanField(default=False)
    url = models.URLField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User, related_name='events_created')
    attendees = models.ManyToManyField(User, through='Attendance', related_name='events_attended')

    objects = EventManager()

    class Meta:
        ordering = ['-start_date']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.id])

class Attendance(models.Model):
    user = models.ForeignKey(User, related_name='event_attendances')
    event = models.ForeignKey(Event, related_name='attendances')
    join_time = models.DateField(auto_now_add=True)
    guests = models.IntegerField(default=0)
    message = models.TextField(blank=True)
