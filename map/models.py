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
    def box(self):
        boxPoints = {}
        extent = self.geom.extent
        boxPoints['nw'] = {'lat': extent[3], 'lon': extent[0]}
        boxPoints['ne'] = {'lat': extent[3], 'lon': extent[2]}
        boxPoints['se'] = {'lat': extent[1], 'lon': extent[2]}
        boxPoints['sw'] = {'lat': extent[1], 'lon': extent[0]}
        return boxPoints

    def isWithinBox(self, point):
        xmin = self.geom.extent[0]
        ymin = self.geom.extent[1]
        xmax = self.geom.extent[2]
        ymax = self.geom.extent[3]
        lat = point.y
        lon = point.x
        return xmin <= lon and lon <= xmax and ymin <= lat and lat <= ymax

# Auto-generated `LayerMapping` dictionary for CityBorder model
cityborder_mapping = {
    'objectid': 'OBJECTID',
    'name': 'NAME',
    'shape_area': 'SHAPE_AREA',
    'shape_len': 'SHAPE_LEN',
    'geom': 'MULTIPOLYGON',
}
