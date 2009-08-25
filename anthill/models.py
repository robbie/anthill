from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from geopy import geocoders

def _geocode(location):
    geocoder = geocoders.Google(settings.GMAPS_API_KEY)
    locations = list(geocoder.geocode(location, exactly_one=False))
    if locations:
        point = locations[0][1]
        return Point(*point), locations[0][0]
    else:
        return None, None

class LocationModelQuerySet(models.query.GeoQuerySet):
    def search_by_distance(self, location, mile_radius):
        point, location_name = _geocode(location)
        if point:
            result = self.filter(lat_long__distance_lte=(point, D(mi=mile_radius))).distance(point).order_by('distance')
        else:
            result = self
        result.geocoded_location = location_name
        return result

class LocationModelManager(models.GeoManager):
    def get_query_set(self):
        return LocationModelQuerySet(self.model)

class LocationModel(models.Model):
    location = models.CharField('description of location, hopefully geocodable (eg. Washington, DC)', max_length=100, blank=True)
    lat_long = models.PointField('geocoded location', null=True, blank=True)

    objects = LocationModelManager()

    def save(self, *args, **kwargs):
        if self.location:
            self.lat_long, _ = _geocode(self.location)
        super(LocationModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
