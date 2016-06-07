from crime.api import CriminalRecordResource
from map.api import CityBorderResource, CityBorderDetailResource
from tastypie.api import Api

api = Api(api_name='api')

api.register(CriminalRecordResource())
api.register(CityBorderDetailResource())
api.register(CityBorderResource())
