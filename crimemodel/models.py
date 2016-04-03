from __future__ import unicode_literals

from django.db import models

from crime.models import Crime
from map.models import Grid


class Crime(Crime):
    grid = models.ForeignKey(Grid, related_name='crimes')
