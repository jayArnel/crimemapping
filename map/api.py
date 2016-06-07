from tastypie.resources import ModelResource
from tastypie import fields

from models import CityBorder


class CityBorderDetailResource(ModelResource):
    class Meta:
        queryset = CityBorder.objects.all()
        resource_name = 'cityborder-detail'
        filtering = {
            "name": "exact",
        }
        excludes = ['geom']


class CityBorderResource(ModelResource):

    geojson = fields.CharField(attribute='geojson', readonly=True)
    center = fields.CharField(attribute='center', readonly=True)
    box = fields.DictField(attribute='box', readonly=True)

    class Meta:
        queryset = CityBorder.objects.all()
        resource_name = 'cityborder'
        filtering = {
            "name": "exact",
        }
