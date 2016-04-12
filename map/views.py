import json

from django.http import HttpResponse
from django.views.generic import TemplateView, View

from map.models import CityBorder
from map.utils import generateGeoJson


class MapView(TemplateView):
    template_name = 'map.html'


class FetchGridView(View):

    def get(self, request, *args, **kwargs):
        pk = self.request.GET.get('pk')
        size = int(self.request.GET.get('size'))
        city = CityBorder.objects.get(pk=pk)
        grid = city.grids.filter(size=size).values_list('geom', flat=True)
        geojson = generateGeoJson(list(grid))
        return HttpResponse(json.dumps(geojson))
