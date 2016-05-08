import cPickle as pickle
import os

from dateutil import rrule
from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Count

from map.models import CityBorder
from crime.models import CriminalRecord

if not hasattr(settings, 'VECTORS_DIR'):
    raise ImproperlyConfigured(
        'The directory to save vector pickles is missing from your settings')
elif not os.path.exists(settings.VECTORS_DIR):
    os.makedirs(settings.VECTORS_DIR)


def vectorize(grid_size, period, crime_type=None, new=False):
    type_verbose = 'ALL' if crime_type is None else crime_type
    file = 'type-{0}_grid_size-{1}_period-{2}.p'.format(
        type_verbose, grid_size, period)
    path = settings.VECTORS_DIR + file
    try:
        if new:
            raise EnvironmentError()
        else:
            vectors = pickle.load(open(path, "rb"))
    except EnvironmentError as e:
        first_data = CriminalRecord.objects.first()
        last_data = CriminalRecord.objects.last()
        start = first_data.date
        end = last_data.date
        city = CityBorder.objects.get(name='Chicago')
        grid = city.generateGrid(grid_size)
        if period == 'daily':
            rule = rrule.DAILY
            extra_query = {
                'day': "EXTRACT(day FROM date)",
                'month': "EXTRACT(month FROM date)",
                'year': "EXTRACT(year FROM date)"
            }
        elif period == 'weekly':
            vectors = vectorize_weekly(grid, crime_type)
        elif period == 'monthly':
            rule = rrule.MONTHLY
            extra_query = {
                'month': "EXTRACT(month FROM date)",
                'year': "EXTRACT(year FROM date)"
            }
        elif period == 'yearly':
            rule = rrule.YEARLY
            extra_query = {
                'year': "EXTRACT(year FROM date)"
            }
        else:
            raise NotImplementedError(
                'Vectorization by "{0}" time step is not yet implemented.'.
                format(period))

        timesteps = {}
        for dt in rrule.rrule(rule, dtstart=start, until=end):
            key = '-'.join([str(getattr(dt, k)) for k in extra_query.keys()])
            timesteps[key] = [0] * len(grid)

        for i in xrange(len(grid)):
            g = grid[i]
            crimes = CriminalRecord.objects.filter(
                location__intersects=g).extra(select=extra_query).values(
                *extra_query.keys()).annotate(count_items=Count('date'))
            for c in crimes:
                key = '-'.join(
                    [str(int(c.get(k))) for k in extra_query.keys()])
                timesteps[key][i] = 1
        vectors = timesteps.values()
        pickle.dump(vectors, open(path, "wb"))
    return vectors


def vectorize_weekly(grid, crime_type=None):
    filters = {}
    if crime_type is not None:
        filters['primary_type'] = crime_type
    first_data = CriminalRecord.objects.first()
    last_data = CriminalRecord.objects.last()
    start = first_data.date
    dtstart = start + timedelta(days=7)
    end = last_data.date
    vectors = []
    for dt in rrule.rrule(rrule.WEEKLY, dtstart=dtstart, until=end):
        vector = []
        print start, dt
        for i in xrange(len(grid)):
            g = grid[i]
            filters['date__range'] = (start, dt)
            filters['location__intersects'] = g
            crimes = CriminalRecord.objects.filter(**filters).count()
            has_crime = 1 if crimes > 0 else 0
            vector.append(has_crime)
        start = dt
        vectors.append(vector)
    return vectors


def generate_all_data(new=False):
    crime_types = list(
        CriminalRecord.objects.order_by('primary_type').distinct().values_list(
            'primary_type', flat=True))
    crime_types.append(None)
    for size in settings.GRID_SIZES:
        for period in settings.PERIODS:
            for crime_type in crime_types:
                print 'generating data for grid cell size: '\
                    '{0}, period: {1}, type: {2}'.format(
                        size, period, crime_type)
                vectorize(size, period, crime_type, new=False)
