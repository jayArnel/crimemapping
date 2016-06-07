import json

from django.http import HttpResponse
from django.views.generic import TemplateView, View

from map.models import CityBorder
from map.utils import generateGeoJson


class FetchGridView(View):
    ''' Fetch grid of a map'''
    def get(self, request, *args, **kwargs):
        '''
        get the grid of the map based on supplied pk, size

        :rtype: HTTPResponse with the dumped geojson
        '''
        pk = self.request.GET.get('pk')
        size = int(self.request.GET.get('size'))
        city = CityBorder.objects.get(pk=pk)
        grid = city.generateGrid(size)
        geojson = generateGeoJson(list(grid))
        return HttpResponse(json.dumps(geojson))
