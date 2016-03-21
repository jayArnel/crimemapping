from django.conf.urls import url, include

import views

urlpatterns = [
    url(r'^fetch/$', views.FetchCrimesView.as_view(), name='fetch-crimes'),
]
