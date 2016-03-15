# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models


class CityBorder(models.Model):
    objectid = models.IntegerField()
    name = models.CharField(max_length=25)
    shape_area = models.FloatField()
    shape_len = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.name

# Auto-generated `LayerMapping` dictionary for CityBorder model
cityborder_mapping = {
    'objectid': 'OBJECTID',
    'name': 'NAME',
    'shape_area': 'SHAPE_AREA',
    'shape_len': 'SHAPE_LEN',
    'geom': 'MULTIPOLYGON',
}
