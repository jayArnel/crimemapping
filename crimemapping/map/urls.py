from django.conf.urls import url, include

import views

urlpatterns = [
    url(r'^$', views.MapView.as_view(), name='home'),
    url(r'^update-database/$', views.UpdateDBView.as_view(), name='update-db'),
]
