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


def vectorize(grid_size, period, crime_type=None, seasonal=False, new=False):
    '''
    Vectorize crime data fetched from the database. The vector is saved to a
        pickle file and then retrieved later

    :param grid_size: size of the cell dimension for the grid
    :param period: timestep of crime data
    :param crime_type: type of crime to be trained, None value will
        train all
    :param seasonal: implement seasonality or not
    :param new: will override the old one pickle file if and if True
    :raises: EnvironmentError, NotImplementedError
    :rtype: returns the resulting vector
    '''
    type_verbose = 'ALL' if crime_type is None else crime_type
    file = 'type-{0}_grid_size-{1}_period-{2}_seasonal-{3}.p'.format(
        type_verbose, grid_size, period, seasonal)
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
            return vectorize_weekly(
                grid, crime_type=crime_type, seasonal=seasonal)
        elif period == 'monthly':
            rule = rrule.MONTHLY
            extra_query = {
                'month': "EXTRACT(month FROM date)",
                'year': "EXTRACT(year FROM date)"
            }
        elif period == 'yearly':
            if seasonal:
                raise NotImplementedError(
                    'Seasonality is not applicable on a yearly period')
            rule = rrule.YEARLY
            extra_query = {
                'year': "EXTRACT(year FROM date)"
            }
        else:
            raise NotImplementedError(
                'Vectorization by "{0}" time step is not yet implemented.'.
                format(period))

        timesteps = {}
        if seasonal:
            for dt in rrule.rrule(rule, dtstart=start, until=end):
                if period == 'daily':
                    season_key = '-'.join(
                        ["%02d" % getattr(dt, k) for k in ['month', 'day']])
                elif period == 'monthly':
                    season_key = '-'.join(
                        ["%02d" % getattr(dt, k) for k in ['month']])
                try:
                    season = timesteps[season_key]
                except KeyError:
                    timesteps[season_key] = {}
                step_key = '-'.join(
                    ["%02d" % getattr(dt, k) for k in ['year']])
                timesteps[season_key][step_key] = [-1] * len(grid)
            for i in xrange(len(grid)):
                g = grid[i]
                crimes = CriminalRecord.objects.filter(
                    location__intersects=g).extra(
                    select=extra_query).values(
                    *extra_query.keys()).annotate(count_items=Count('date'))
                for c in crimes:
                    if period == 'daily':
                        season_key = '-'.join(
                            ["%02d" % c.get(k) for k in ['month', 'day']])
                    elif period == 'monthly':
                        season_key = '-'.join(
                            ["%02d" % c.get(k) for k in ['month']])
                    step_key = '-'.join(
                        ["%02d" % c.get(k) for k in ['year']])
                    timesteps[season_key][step_key][i] = 1
            vectors = []
            for k1 in sorted(timesteps):
                season = []
                for k2 in sorted(timesteps[k1]):
                    season.append(timesteps[k1][k2])
                vectors.append(season)

        else:
            for dt in rrule.rrule(rule, dtstart=start, until=end):
                key = '-'.join(
                    ["%02d" % getattr(dt, k) for k in extra_query.keys()])
                timesteps[key] = [-1] * len(grid)

            for i in xrange(len(grid)):
                g = grid[i]
                crimes = CriminalRecord.objects.filter(
                    location__intersects=g, date__lte=end).extra(
                    select=extra_query).values(
                    *extra_query.keys()).annotate(count_items=Count('date'))
                for c in crimes:
                    key = '-'.join(
                        ["%02d" % c.get(k) for k in extra_query.keys()])
                    timesteps[key][i] = 1
            vectors = []
            for k1 in sorted(timesteps):
                vectors.append(timesteps[k1])
        pickle.dump(vectors, open(path, "wb"))
    return vectors


def vectorize_weekly(grid, crime_type=None, seasonal=False):
    '''
    Special vectorization for weekly data

    :param grid_size: size of the cell dimension for the grid
    :param crime_type: type of crime to be trained, None value will
        train all
    :param seasonal: implement seasonality or not
    :rtype: returns the resulting vector
    '''
    filters = {}
    if crime_type is not None:
        filters['primary_type'] = crime_type
    first_data = CriminalRecord.objects.first()
    last_data = CriminalRecord.objects.last()
    start = first_data.date
    dtstart = start + timedelta(days=7)
    end = last_data.date
    if seasonal:
        timesteps = {}
        for dt in rrule.rrule(rrule.WEEKLY, dtstart=dtstart, until=end):
            season_key = '-'.join(
                ["%02d" % getattr(start, k) for k in ['month', 'day']])
            try:
                season = timesteps[season_key]
            except KeyError:
                timesteps[season_key] = []
            vector = []
            for i in xrange(len(grid)):
                g = grid[i]
                filters['date__range'] = (start, dt)
                filters['date__lte'] = end
                filters['location__intersects'] = g
                crimes = CriminalRecord.objects.filter(**filters).count()
                has_crime = 1 if crimes > 0 else -1
                vector.append(has_crime)
            start = dt
            timesteps[season_key].append(vector)
        print timesteps
        vectors = []
        for k1 in sorted(timesteps):
            vectors.append(timesteps[k1])
    else:
        vectors = []
        for dt in rrule.rrule(rrule.WEEKLY, dtstart=dtstart, until=end):
            vector = []
            for i in xrange(len(grid)):
                g = grid[i]
                filters['date__range'] = (start, dt)
                filters['location__intersects'] = g
                crimes = CriminalRecord.objects.filter(**filters).count()
                has_crime = 1 if crimes > 0 else -1
                vector.append(has_crime)
            start = dt
            vectors.append(vector)
    return vectors


def _generate_all_vectors(new=False):
    crime_types = list(CriminalRecord.objects.values('primary_type').annotate(
        count=Count('primary_type')).order_by('-count').values_list(
        'primary_type', flat=True)[:3])
    crime_types.append(None)
    for crime_type in crime_types:
        for size in settings.GRID_SIZES:
            for period in settings.PERIODS:
                print 'generating data for grid cell dimension: '\
                    '{0} meters, period: {1}, type: {2} and '\
                    'seasonality: True'.format(size, period, crime_type)
                vectorize(size, period, crime_type=crime_type,
                          seasonal=True, new=new)
                print 'generating data for grid cell dimension: '\
                    '{0} meters, period: {1}, type: {2} and '\
                    'seasonality: False'.format(size, period, crime_type)
                vectorize(size, period, crime_type=crime_type,
                          seasonal=False, new=new)
