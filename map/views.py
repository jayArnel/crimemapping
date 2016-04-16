import json

from django.http import HttpResponse
from django.views.generic import TemplateView, View

from crime.models import CriminalRecord
from map.models import CityBorder
from map.utils import generateGeoJson


class MapView(TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        context = {}
        crimes = CriminalRecord.objects.all()
        context['crime_types'] = crimes.order_by(
            'primary_type').distinct().values_list('primary_type', flat=True)
        context['start'] = str(crimes.order_by('date').first().date.date())
        context['end'] = str(crimes.order_by('date').last().date.date())
        return context


class FetchGridView(View):

    def get(self, request, *args, **kwargs):
        pk = self.request.GET.get('pk')
        size = int(self.request.GET.get('size'))
        city = CityBorder.objects.get(pk=pk)
        grid = city.generateGrid(size)
        geojson = generateGeoJson(list(grid))
        return HttpResponse(json.dumps(geojson))
