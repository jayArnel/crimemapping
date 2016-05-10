from django.conf.urls import url, include
from django.contrib import admin

from map import urls as map_urls
from crime import urls as crime_urls
from api import api

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^crime/', include(crime_urls)),
    url(r'^map/', include(map_urls)),
    url(r'', include(api.urls)),
]
