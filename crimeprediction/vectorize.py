import cPickle as pickle

from map.models import CityBorder
from crime.models import CriminalRecord


def vectorize(grid_size, period, new=False):
    file = str(grid_size) + 'grid_size_' + period + 'period_vector.p'
    if new:
        try:
            vectors = pickle.load(open(file, "rb"))
        except (OSError, IOError) as e:
            city = CityBorder.objects.get(name='Chicago')
            grid = city.generateGrid(grid_size)
            vectors = []
            first_data = CriminalRecord.objects.first()
            last_data = CriminalRecord.objects.last()
            first_year = first_data.date.year
            first_month = first_data.date.month
            last_year = last_data.date.year
            last_month = last_data.date.month
            start = 12 * first_year + first_month - 1
            end = 12 * last_year + last_month
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
            pickle.dump(vectors, open(file, "wb"))
        return vectors
    else:
        city = CityBorder.objects.get(name='Chicago')
        grid = city.generateGrid(grid_size)
        vectors = []
        first_data = CriminalRecord.objects.first()
        last_data = CriminalRecord.objects.last()
        first_year = first_data.date.year
        first_month = first_data.date.month
        last_year = last_data.date.year
        last_month = last_data.date.month
        start = 12 * first_year + first_month - 1
        end = 12 * last_year + last_month
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
        pickle.dump(vectors, open(file, "wb"))
        return vectors
