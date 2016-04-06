from __future__ import unicode_literals

from django.apps import AppConfig


class CrimeModelConfig(AppConfig):
    name = 'crimemodel'

    def ready(self):
        import crimemodel.signals
