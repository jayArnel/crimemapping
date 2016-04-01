# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, LinearRing, Polygon
from django.core.serializers import serialize

from map.utils import getNextPoint


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

    def generateGrid(self, size):
        grid = []
        start = Point(self.box['nw']['lon'], self.box['nw']['lat'])
        lat = lon = start
        while self.isWithinBox(lat):
            nw = lat
            ne = getNextPoint(nw, size, 90)
            sw = getNextPoint(nw, size, 180)
            se = getNextPoint(ne, size, 180)
            lat = ne
            linearRing = LinearRing(nw, ne, se, sw, nw)
            polygon = Polygon(linearRing)
            if polygon.intersects(self.geom):
                grid.append(polygon)
            if not self.isWithinBox(lat):
                lon = getNextPoint(lon, size, 180)
                lat = lon
        return grid

# Auto-generated `LayerMapping` dictionary for CityBorder model
cityborder_mapping = {
    'objectid': 'OBJECTID',
    'name': 'NAME',
    'shape_area': 'SHAPE_AREA',
    'shape_len': 'SHAPE_LEN',
    'geom': 'MULTIPOLYGON',
}
