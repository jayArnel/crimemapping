from datetime import datetime

from sodapy import Socrata

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from crimemapping.crime.models import Crime
# Create your views here.


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context={}, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(self.get_data(context), **response_kwargs)

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class MapView(TemplateView):
    template_name = 'map.html'


class UpdateDBView(JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        ids = Crime.objects.values_list('case_id', flat=True)
        domain = settings.SOCRATA_DOMAIN
        token = settings.SOCRATA_APP_TOKEN
        endpoint = settings.SOCRATA_DATASET_ENDPOINT
        client = Socrata(domain, token)
        order = "date"
        where = 'latitude IS NOT NULL'
        offset = 0
        limit = 1000
        status = 200
        try:
            data = client.get(
                endpoint, order=order, where=where, offset=offset, limit=limit)
            while data:
                for record in data:
                    if self.to_int(record.get('id')) not in ids:
                        attrs = {
                            'case_id': self.to_int(
                                self.get_from_dict(record, 'id')),
                            'case_number': self.get_from_dict(
                                record, 'case_number'),
                            'date': datetime.strptime(
                                self.get_from_dict(record, 'date'),
                                '%Y-%m-%dT%H:%M:%S'),
                            'block': self.get_from_dict(record, 'block'),
                            'iucr': self.get_from_dict(record, 'iucr'),
                            'primary_type': self.get_from_dict(
                                record, 'primary_type'),
                            'crime_description': self.get_from_dict(
                                record, 'description'),
                            'location_description': self.get_from_dict(
                                record, 'location_description'),
                            'has_arrested': self.get_from_dict(
                                record, 'arrest'),
                            'is_domestic': self.get_from_dict(
                                record, 'domestic'),
                            'beat': self.get_from_dict(record, 'beat'),
                            'district': self.get_from_dict(record, 'district'),
                            'ward': self.to_int(
                                self.get_from_dict(record, 'ward')),
                            'community_area': self.get_from_dict(
                                record, 'community_area'),
                            'fbi_code': self.get_from_dict(record, 'fbi_code'),
                            'x_coordinate': self.to_int(
                                self.get_from_dict(record, 'x_coordinate')),
                            'y_coordinate': self.to_int(
                                self.get_from_dict(record, 'y_coordinate')),
                            'year': self.to_int(
                                self.get_from_dict(record, 'year')),
                            'updated_on': datetime.strptime(
                                self.get_from_dict(record, 'updated_on'),
                                '%Y-%m-%dT%H:%M:%S'),
                            'latitude': float(self.get_from_dict(
                                record, 'latitude')),
                            'longitude': float(self.get_from_dict(
                                record, 'longitude')),
                        }
                        c = Crime.objects.create(**attrs)
                offset += limit
                data = client.get(
                    endpoint, order=order, where=where,
                    offset=offset, limit=limit)
            client.close()
        except Exception, e:
            print e
            status = 400
        return self.render_to_json_response(status=status)

    def get_from_dict(self, dic, key):
        return dic.get(key) if dic.get(key) else ''

    def to_int(self, data):
        num = data.strip()
        return int(num) if num else None
