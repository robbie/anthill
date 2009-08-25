from django.contrib.gis import admin
from anthill.people.models import Profile

admin.site.register(Profile, admin.OSMGeoAdmin)
