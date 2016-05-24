from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^(?P<name>[\w-]+)/$', views.MapView.as_view(), name='map'),
]
