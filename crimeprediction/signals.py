from django.db.models.signals import post_save
from django.dispatch import receiver

from crime.models import CriminalRecord
from crimeprediction.models import CrimeSample
from map.models import Grid


@receiver(post_save, sender=CriminalRecord)
def createCrimeSamples(sender, instance, created, *args, **kwargs):
    grids = Grid.objects.filter(geom__intersects=instance.location)
    sample, created = CrimeSample.objects.get_or_create(crime=instance)
    if created:
        sample.grids.add(*list(grids))
