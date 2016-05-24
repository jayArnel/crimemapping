from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from crime.models import CriminalRecord
from map.models import CityBorder


class HomeView(TemplateView):
    template_name = 'home/home.html'


class MapView(TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        context = {}
        city = get_object_or_404(CityBorder, name=kwargs['name'])
        crimes = CriminalRecord.objects.all()
        context['crime_types'] = crimes.order_by(
            'primary_type').distinct().values_list('primary_type', flat=True)
        context['start'] = str(crimes.order_by('date').first().date.date())
        context['end'] = str(crimes.order_by('date').last().date.date())
        return context
