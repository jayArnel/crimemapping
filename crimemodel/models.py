from __future__ import unicode_literals

from django.db import models

from crime import models


class Crime(models.Crime):
    grid = models.ForeignKey('Grid', related_name='crimes')
