from django.conf.urls import url, include

import views

urlpatterns = [
    url(r'^(?P<name>[\w-]+)/$', views.MapView.as_view(), name='map'),
    url(r'^grid/$', views.FetchGridView.as_view(), name='grid'),
]
