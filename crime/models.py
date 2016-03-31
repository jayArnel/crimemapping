from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Crime(models.Model):
    """ a model for a single criminal record """
    case_id = models.IntegerField()
    case_number = models.CharField(max_length=10)
    date = models.DateTimeField()
    block = models.CharField(max_length=50)
    iucr = models.CharField(max_length=4)
    primary_type = models.CharField(max_length=50)
    crime_description = models.CharField(max_length=100)
    location_description = models.CharField(max_length=100)
    has_arrested = models.BooleanField()
    is_domestic = models.BooleanField()
    beat = models.CharField(max_length=4)
    district = models.CharField(max_length=3)
    ward = models.IntegerField(null=True)
    community_area = models.CharField(max_length=2, blank=True)
    fbi_code = models.CharField(max_length=3)
    x_coordinate = models.IntegerField()
    y_coordinate = models.IntegerField()
    year = models.IntegerField()
    updated_on = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        app_label = "crime"