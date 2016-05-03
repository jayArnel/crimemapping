import cPickle as pickle
from dateutil import rrule
from datetime import datetime, timedelta
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from map.models import CityBorder
from crime.models import CriminalRecord

if not hasattr(settings, 'VECTORS_DIR'):
    raise ImproperlyConfigured(
        'The directory to save vector pickles is missing from your settings')
elif not os.path.exists(settings.VECTORS_DIR):
    os.makedirs(settings.VECTORS_DIR)


def vectorize(grid_size, period, crime_type=None, new=False):
    file = 'type-{0}_grid_size-{1}_period-{2}.p'.format(
        'ALL' if crime_type is None, grid_size, period)
    path = settings.VECTORS_DIR + file
    try:
        if new:
            raise EnvironmentError()
        else:
            vectors = pickle.load(open(path, "rb"))
    except EnvironmentError as e:
        city = CityBorder.objects.get(name='Chicago')
        grid = city.generateGrid(grid_size)
        if period == 'monthly':
            vectors = vectorize_monthly(grid, crime_type)
        elif period == 'yearly':
            vectors = vectorize_yearly(grid, crime_type)
        elif period == 'weekly':
            vectors = vectorize_weekly(grid, crime_type)
        else:
            raise NotImplementedError(
                'Vectorization by "{0}" time step is not yet implemented.'.
                format(period))
        pickle.dump(vectors, open(path, "wb"))
    return vectors


def vectorize_monthly(grid, crime_type=None):
    filters = {}
    if crime_type is not None:
        filters['primary_type'] = crime_type
    first_data = CriminalRecord.objects.first()
    last_data = CriminalRecord.objects.last()
    first_year = first_data.date.year
    first_month = first_data.date.month
    last_year = last_data.date.year
    last_month = last_data.date.month
    start = 12 * first_year + first_month - 1
    end = 12 * last_year + last_month
    vectors = []
    for ym in range(start, end):
        year, month = divmod(ym, 12)
        month += 1
        print year, month
        vector = []
        for i in xrange(len(grid)):
            g = grid[i]
            filters['date__month'] = month
            filters['date__year'] = year
            filters['location__intersects'] = g
            crimes = CriminalRecord.objects.filter(**filters).count()
            has_crime = int(crimes > 0)
            vector.append(has_crime)
        vectors.append(vector)
    return vectors


def vectorize_yearly(grid, crime_type=None):
    filters = {}
    if crime_type is not None:
        filters['primary_type'] = crime_type
    first_data = CriminalRecord.objects.first()
    last_data = CriminalRecord.objects.last()
    first_year = first_data.date.year
    last_year = last_data.date.year
    vectors = []
    for year in range(first_year, last_year + 1):
        print year
        vector = []
        for i in xrange(len(grid)):
            g = grid[i]
            filters['date__year'] = year
            filters['location__intersects'] = g
            crimes = CriminalRecord.objects.filter(**filters).count()
            has_crime = int(crimes > 0)
            vector.append(has_crime)
        vectors.append(vector)
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
            has_crime = int(crimes > 0)
            vector.append(has_crime)
        start = dt
        vectors.append(vector)
    return vectors


def generate_all_data(new=False):
    crime_types = list(
        CriminalRecord.objects.order_by('primary_type').distinct().values_list(
            'primary_type', flat=True))
    for size in settings.GRID_SIZES:
        for period in settings.PERIODS:
            for crime_type in crime_types:
                vectorize(size, period, crime_type, new=False)
