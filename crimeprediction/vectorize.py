from map.models import CityBorder
from crime.models import CriminalRecord


def vectorize():
    city = CityBorder.objects.get(name='Chicago')
    grid = city.generateGrid(1000)
    vectors = []
    first_data = CriminalRecord.objects.first()
    month = first_data.date.month
    year = first_data.date.year
    last_data = CriminalRecord.objects.last()
    last_month = last_data.date.month
    last_year = last_data.date.year
    while year <= last_year:
        while month <= last_month and month <= 12:
            print 'month: ' + str(month), 'year: ' + str(year)
            vector = [(month, year)]
            for i in xrange(len(grid)):
                g = grid[i]
                crimes = CriminalRecord.objects.filter(
                    date__month=month, date__year=year,
                    location__intersects=g).count()
                has_crime = int(crimes > 0)
                print('grid: ' + str(i), 'count: ' + str(crimes),
                      'has_crime: ' + str(has_crime))
                vector.append(has_crime)
            vectors.append(vector)
            month += 1
        year += 1
    print vectors
    return vectors
