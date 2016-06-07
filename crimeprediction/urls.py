from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^map/(?P<name>[\w-]+)/$', views.MapView.as_view(), name='map'),
    url(r'^dashboard/(?P<name>[\w-]+)/$',
        views.DashboardView.as_view(), name='dashboard'),
    url(r'^train/$', views.TrainView.as_view(), name='train'),
    url(r'^predict/$', views.PredictView.as_view(), name='predict'),
]
