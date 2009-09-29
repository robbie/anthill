from django.contrib.gis import admin
from anthill.events.models import Event, Attendance

class AttendanceInline(admin.TabularInline):
    model = Attendance

class EventAdmin(admin.OSMGeoAdmin):
    inlines = [AttendanceInline,]

admin.site.register(Event, EventAdmin)