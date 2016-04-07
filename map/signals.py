from django.conf import settings
from django.contrib.gis.geos import Point, LinearRing, Polygon
from django.db.models.signals import post_save
from django.dispatch import receiver

from map.models import CityBorder, Grid
from map.utils import getNextPoint


@receiver(post_save, sender=CityBorder)
def generateGrid(sender, instance, created, *args, **kwargs):
    grids = []
    for size in settings.GRID_SIZES:
        count = 0
        start = Point(instance.box['nw']['lon'], instance.box['nw']['lat'])
        lat = lon = start
        while instance.geom.envelope.intersects(lat):
            nw = lat
            ne = getNextPoint(nw, size, 90)
            sw = getNextPoint(nw, size, 180)
            se = getNextPoint(ne, size, 180)
            lat = ne
            linearRing = LinearRing(nw, ne, se, sw, nw)
            polygon = Polygon(linearRing)
            if polygon.intersects(instance.geom):
                count += 1
                attrs = {
                    'city': instance,
                    'number': count,
                    'size': size,
                    'geom': polygon,
                }
                grid = Grid(**attrs)
                grids.append(grid)
            if not instance.geom.envelope.intersects(lat):
                lon = getNextPoint(lon, size, 180)
                lat = lon
    Grid.objects.bulk_create(grids)
