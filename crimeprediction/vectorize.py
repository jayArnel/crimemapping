import cPickle as pickle
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


def vectorize(grid_size, period, new=False):
    file = str(grid_size) + 'grid_size_' + period + 'period_vector.p'
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
            vectors = vectorize_monthly(grid)
        if period == 'yearly':
            vectors = vectorize_yearly(grid)
        else:
            raise NotImplementedError(
                'Vectorization by "{0}" time step is not yet implemented.'\
                .format(period))
        pickle.dump(vectors, open(path, "wb"))
    return vectors

def vectorize_monthly(grid):
    first_data = CriminalRecord.objects.first()
    last_data = CriminalRecord.objects.last()
    first_year = first_data.date.year
    first_month = first_data.date.month
    last_year = last_data.date.year
    last_month = last_data.date.month
    start = 12 * first_year + first_month - 1
    end = 12 * last_year + last_month
    vectors = []
    for ym in range(start, end ):
        year, month = divmod( ym, 12 )
        month += 1
        print year, month
        vector = []
        for i in xrange(len(grid)):
            g = grid[i]
            crimes = CriminalRecord.objects.filter(
                date__month=month, date__year=year,
                location__intersects=g).count()
            has_crime = int(crimes > 0)
            vector.append(has_crime)
        vectors.append(vector)
    return vectors

def vectorize_yearly(grid):
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
            crimes = CriminalRecord.objects.filter(
                date__year=year, location__intersects=g).count()
            has_crime = int(crimes > 0)
            vector.append(has_crime)
        vectors.append(vector)
    return vectors