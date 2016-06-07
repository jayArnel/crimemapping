'''
    API resources for the Crime module
'''

from tastypie.resources import ModelResource
from models import CriminalRecord


class CriminalRecordResource(ModelResource):
    '''Api resource for CriminalRecord Model'''
    class Meta:
        queryset = CriminalRecord.objects.all().order_by('date')
        resource_name = 'criminalrecord'
        filtering = {
            'primary_type': ['exact', 'in'],
            'date': ['range', 'exact', 'gt', 'gte', 'lt', 'lte'],
        }
