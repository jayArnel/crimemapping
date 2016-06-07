from django.conf import settings
from django.db.models import Count

from crime.models import CriminalRecord
from crimeprediction.network import run_network


def run_experiments():
    '''
    Perfrom all experiments by running network under all possible conditions
    '''
    crime_types = list(CriminalRecord.objects.values('primary_type').annotate(
        count=Count('primary_type')).order_by('-count').values_list(
        'primary_type', flat=True)[:3])
    crime_types.append(None)
    for crime_type in crime_types:
        for size in settings.GRID_SIZES:
            for period in settings.PERIODS:
                kwargs = {
                    'grid_size': size,
                    'period': period,
                    'crime_type': crime_type,
                }
                if period != 'yearly':
                    kwargs['seasonal'] = True
                    print 'experiment for grid cell dimension: '\
                        '{0} meters, period: {1}, type: {2} and '\
                        'seasonality: True'.format(size, period, crime_type)
                    run_network(**kwargs)
                print 'experiment for grid cell dimension: '\
                    '{0} meters, period: {1}, type: {2} and '\
                    'seasonality: False'.format(size, period, crime_type)
                kwargs['seasonal'] = False
                run_network(**kwargs)
