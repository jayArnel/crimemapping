from tastypie.resources import ModelResource
from crimemapping.crime.models import Crime


class CrimeResource(ModelResource):
    class Meta:
        queryset = Crime.objects.all()
        resource_name = 'crime'
