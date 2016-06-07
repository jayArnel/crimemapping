import os
import yaml

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from crime.models import CriminalRecord
from map.models import CityBorder


class HomeView(TemplateView):
    template_name = 'home/home.html'


class MapView(TemplateView):
    template_name = 'map/map.html'

    def get_context_data(self, **kwargs):
        context = {}
        city = get_object_or_404(CityBorder, name=kwargs['name'])
        crimes = CriminalRecord.objects.all()
        context['crime_types'] = crimes.order_by(
            'primary_type').distinct().values_list('primary_type', flat=True)
        context['start'] = str(crimes.order_by('date').first().date.date())
        context['end'] = str(crimes.order_by('date').last().date.date())
        return context


class DashboardView(TemplateView):
    template_name = 'map/dashboard.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['has_model'] = bool(
            os.path.exists(settings.MODEL_DIR + settings.MODEL_ARCHITECTURE)
            and os.path.exists(settings.MODEL_DIR + settings.MODEL_WEIGHTS))
        if context['has_model']:
            params_file = settings.MODEL_DIR + settings.MODEL_PARAMS
            params = yaml.safe_load(open(params_file).read())
            context.update(params)
        crimes = CriminalRecord.objects.all()
        context['crime_types'] = crimes.order_by(
            'primary_type').distinct().values_list('primary_type', flat=True)
        context['grid_sizes'] = settings.GRID_SIZES
        context['periods'] = settings.PERIODS
        return context
