'''
    Views for the Crime module
'''
from datetime import datetime

from sodapy import Socrata

from django.conf import settings
from django.contrib.gis.geos import Point
from django.http import HttpResponse
from django.views.generic import View

from crime.models import CriminalRecord


class FetchCrimesView(View):
    ''' Fetch criminal records from online data portal '''
    def get(self, request, *args, **kwargs):
        ''' Get criminal records from the dataset and save them the database as CriminalRecord objects'''
        ids = CriminalRecord.objects.values_list('case_id', flat=True)
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
                endpoint, order=order, where=where,
                offset=offset, limit=limit)
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
                            'district': self.get_from_dict(
                                record, 'district'),
                            'ward': self.to_int(
                                self.get_from_dict(record, 'ward')),
                            'community_area': self.get_from_dict(
                                record, 'community_area'),
                            'fbi_code': self.get_from_dict(
                                record, 'fbi_code'),
                            'x_coordinate': self.to_int(
                                self.get_from_dict(
                                    record, 'x_coordinate')),
                            'y_coordinate': self.to_int(
                                self.get_from_dict(
                                    record, 'y_coordinate')),
                            'year': self.to_int(
                                self.get_from_dict(record, 'year')),
                            'updated_on': datetime.strptime(
                                self.get_from_dict(record, 'updated_on'),
                                '%Y-%m-%dT%H:%M:%S'),
                            'latitude': float(self.get_from_dict(
                                record, 'latitude')),
                            'longitude': float(self.get_from_dict(
                                record, 'longitude')),
                            'location': Point(
                                float(self.get_from_dict(
                                    record, 'longitude')),
                                float(self.get_from_dict(
                                    record, 'latitude')))
                        }
                        CriminalRecord.objects.create(**attrs)
                offset += limit
                data = client.get(
                    endpoint, order=order, where=where,
                    offset=offset, limit=limit)
            client.close()
        except Exception, e:
            print e
            status = 400
        return HttpResponse(status=status)

    def get_from_dict(self, dic, key):
        '''
        get an value from the dictionary using a key but instead of None
        return an empty string if it does not exist

        :param dic: the dictionary to be search
        :param key: key of the value to be obtained
        :rtype: value of the key in the dictionary or empty string
        '''

        return dic.get(key) if dic.get(key) else ''

    def to_int(self, data):
        '''
        converts data to interger, return None instead of number

        :param data: data to be converted
        :rtype: interger converstion of the data or None
        '''
        num = data.strip()
        return int(num) if num else None
