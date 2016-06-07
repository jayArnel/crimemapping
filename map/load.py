import os
from django.contrib.gis.utils import LayerMapping
from models import CityBorder

cityborder_mapping = {
    'objectid': 'OBJECTID',
    'name': 'NAME',
    'shape_area': 'SHAPE_AREA',
    'shape_len': 'SHAPE_LEN',
    'geom': 'MULTIPOLYGON',
}

city_shp = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'data', 'boundaries', 'City_Boundary.shp'))


def run(verbose=True):
    ''' load the shape files to the database

    :param verbose: control message outputs of the method
    '''
    lm = LayerMapping(CityBorder, city_shp, cityborder_mapping,
                      transform=True, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose)
