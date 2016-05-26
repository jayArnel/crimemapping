from django.conf.urls import url, include

import views

urlpatterns = [
    url(r'^grid/$', views.FetchGridView.as_view(), name='grid'),
]
