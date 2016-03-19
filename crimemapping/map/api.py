from tastypie.resources import ModelResource
from tastypie import fields

from crimemapping.map.models import CityBorder


class CityBorderResource(ModelResource):

    geojson = fields.CharField(attribute='geojson', readonly=True)
    center = fields.CharField(attribute='center', readonly=True)
    bounds = fields.DictField(attribute='bounds', readonly=True)

    class Meta:
        queryset = CityBorder.objects.all()
        resource_name = 'cityborder'
        filtering = {
            "name": "exact",
        }
