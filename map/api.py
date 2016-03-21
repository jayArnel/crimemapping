from tastypie.resources import ModelResource
from tastypie import fields

from models import CityBorder


class CityBorderResource(ModelResource):

    geojson = fields.CharField(attribute='geojson', readonly=True)

    class Meta:
        queryset = CityBorder.objects.all()
        resource_name = 'cityborder'
        filtering = {
            "name": "exact",
        }
