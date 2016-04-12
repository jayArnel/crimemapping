import yaml

from geopy import distance, Point

from django.contrib.gis import geos


def getNextPoint(point, offset, bearing):
    lat = point.y
    lon = point.x
    pnt = Point(latitude=lat, longitude=lon)
    d = distance.VincentyDistance(meters=offset)
    newPnt = d.destination(point=pnt, bearing=bearing)
    return geos.Point(newPnt.longitude, newPnt.latitude)


def generateGeoJson(geometry):
    if type(geometry) != list:
        geometry = [geometry]
    features = []
    for geom in geometry:
        if isinstance(geom, geos.GEOSGeometry):
            geom_json = yaml.safe_load(geom.json)
            feature = {
                "type": "Feature",
                "geometry": geom_json,
                "properties": {
                    "name": geom_json['type']
                }
            }
            features.append(feature)
        else:
            raise TypeError("Can't generate GeoJSON. " +
                            str(geom) + 'is not geometry.')

    return {"type": "FeatureCollection", "features": features}
