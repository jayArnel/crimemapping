# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models
from django.core.serializers import serialize


class CityBorder(models.Model):
    objectid = models.IntegerField()
    name = models.CharField(max_length=25)
    shape_area = models.FloatField()
    shape_len = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.name

    @property
    def geojson(self):
        return serialize(
            'geojson', CityBorder.objects.filter(pk=self.pk),
            geometry_field='geom', fields=('name',))

    @property
    def center(self):
        return self.geom.centroid.geojson

    @property
    def bounds(self):
        bounds = {}
        extent = self.geom.extent
        bounds['nw'] = [extent[3], extent[0]]
        bounds['ne'] = [extent[3], extent[2]]
        bounds['se'] = [extent[1], extent[2]]
        bounds['sw'] = [extent[1], extent[0]]
        return bounds

# Auto-generated `LayerMapping` dictionary for CityBorder model
cityborder_mapping = {
    'objectid': 'OBJECTID',
    'name': 'NAME',
    'shape_area': 'SHAPE_AREA',
    'shape_len': 'SHAPE_LEN',
    'geom': 'MULTIPOLYGON',
}
