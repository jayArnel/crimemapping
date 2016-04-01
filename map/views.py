import json

from django.http import JsonResponse
from django.http import HttpResponse
from django.views.generic import TemplateView, View

from map.models import CityBorder
from map.utils import generateGeoJson


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


class FetchGridView(JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        pk = self.request.GET.get('pk')
        size = int(self.request.GET.get('size'))
        city = CityBorder.objects.get(pk=pk)
        grid = city.generateGrid(size)
        geojson = generateGeoJson(grid)
        return HttpResponse(json.dumps(geojson))
