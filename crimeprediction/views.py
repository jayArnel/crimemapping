import json
import os
import yaml

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View

from crime.models import CriminalRecord
from crimeprediction.network import(
    run_network, get_trained_model, predict_next)
from map.models import CityBorder


class HomeView(TemplateView):
    '''
    View for the home page
    '''
    template_name = 'home/home.html'


class MapView(TemplateView):
    '''
    View for showing the map
    '''
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
    '''
    View for viewing dashboard or interface for the model
    '''
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


class TrainView(View):
    '''
    View for training a model whose parameters are chosen via web interface
    '''
    def get(self, request, *args, **kwargs):
        crime_type = self.request.GET.get('crime_type')
        grid_size = self.request.GET.get('grid_size')
        period = self.request.GET.get('period')
        seasonality = self.request.GET.get('seasonality')
        seasonal = True if seasonality == 'true' else False
        run_network(
            grid_size, period, crime_type=crime_type, seasonal=seasonal)
        return HttpResponse(status=200)


class PredictView(View):
    '''
    View for generating prediction of next hotspot
    '''
    def get(self, request, *args, **kwargs):
        model, params = get_trained_model()
        msg = {}
        msg['prediction'] = predict_next(model, **params)
        return HttpResponse(json.dumps(msg))
