from map.models import CityBorder
from crime.models import CriminalRecord


def vectorize(grid_size=1000, period='monthly'):
    city = CityBorder.objects.get(name='Chicago')
    grid = city.generateGrid(grid_size)
    vectors = []
    first_data = CriminalRecord.objects.first()
    last_data = CriminalRecord.objects.last()
    first_year = first_data.date.year
    first_month = first_data.date.month
    last_year = 2003
    last_month = 3
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
    return vectors
