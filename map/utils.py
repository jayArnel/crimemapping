import geopy
from geopy import distance

from django.contrib.gis import geos


def getNextPoint(point, offset, bearing):
    lat = point.y
    lon = point.x
    pnt = geopy.Point(latitude=lat, longitude=lon)
    d = distance.VincentyDistance(kilometers=offset)
    newPnt = d.destination(point=pnt, bearing=bearing)
    return geos.Point(newPnt.longitude, newPnt.latitude)
