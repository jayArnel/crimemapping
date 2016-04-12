from __future__ import unicode_literals

from django.db import models

from crime.models import CriminalRecord
from map.models import Grid


class CrimeSample(models.Model):
    crime = models.OneToOneField(CriminalRecord, related_name='sample')
    grids = models.ManyToManyField(Grid, related_name='samples')
