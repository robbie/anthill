from django.contrib.gis import admin
from anthill.events.models import Event

admin.site.register(Event, admin.OSMGeoAdmin)

