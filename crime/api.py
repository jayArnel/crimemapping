from tastypie.resources import ModelResource
from models import CriminalRecord


class CriminalRecordResource(ModelResource):
    class Meta:
        queryset = CriminalRecord.objects.all()
        resource_name = 'crime'
