from tastypie.resources import ModelResource
from tastypie import fields

from models import CityBorder


class CityBorderDetailResource(ModelResource):
    '''API resource for the details of the city border'''
    class Meta:
        queryset = CityBorder.objects.all()
        resource_name = 'cityborder-detail'
        filtering = {
            "name": "exact",
        }
        excludes = ['geom']


class CityBorderResource(ModelResource):
    '''API resource for the geographical information of the city border'''
    geojson = fields.CharField(attribute='geojson', readonly=True)
    center = fields.CharField(attribute='center', readonly=True)
    box = fields.DictField(attribute='box', readonly=True)

    class Meta:
        queryset = CityBorder.objects.all()
        resource_name = 'cityborder'
        filtering = {
            "name": "exact",
        }
