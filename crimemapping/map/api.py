from tastypie.resources import ModelResource
from crimemapping.map.models import CityBorder


class CityBorderResource(ModelResource):
    class Meta:
        queryset = CityBorder.objects.all()
        resource_name = 'cityborder'
