from __future__ import unicode_literals

from django.apps import AppConfig


class CrimePredictionConfig(AppConfig):
    name = 'crimeprediction'
    verbose_name = 'Crime Prediction'

    def ready(self):
        import crimeprediction.signals
