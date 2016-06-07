'''
    Utility methods to generate GeoJSON files and compute distances
'''
import yaml

from geopy import distance, Point

from django.contrib.gis import geos


def getNextPoint(point, offset, bearing):
    '''
    get next point from the given point at a distance and bearing

    :param point: point to be based upon the next point
    :param offset: the distance to be calculated to get the next point
    :param bearing: the direction or angle to where the next point will be calculated
    :rtype: GEOS Point representing the longitude and latitude of the new point
    '''
    lat = point.y
    lon = point.x
    pnt = Point(latitude=lat, longitude=lon)
    d = distance.VincentyDistance(meters=offset)
    newPnt = d.destination(point=pnt, bearing=bearing)
    return geos.Point(newPnt.longitude, newPnt.latitude)


def generateGeoJson(geometry):
    '''
    generate GeoJSON from a geomtry for easy plotting of the borders

    :param geometry: the generated GeoJSON of a geometry
    :rtpye: GeoJson format of geometry
    '''

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
