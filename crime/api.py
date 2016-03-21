from tastypie.resources import ModelResource
from models import Crime


class CrimeResource(ModelResource):
    class Meta:
        queryset = Crime.objects.all()
        resource_name = 'crime'
