require([
    'model','jquery', 'mustache', 'strftime', 'map/js/overlay/overlay',
    'text!mustachetemplates/crime-info.html', 'map/js/menu/menu', 'gmaps'
], function(Model, $, Mustache, strftime, overlay, crimeInfoTemplate) {
    /*
      Initialize variables
     */
    var map = new google.maps.Map(document.getElementById('map'), {
        mapTypeControlOptions: {
            position: google.maps.ControlPosition.TOP_RIGHT,
        }
    });

    var crimeMarkers = {};
    var grid = [];

    var Crimes = new Model('criminalrecord');
    var CityBorder = new Model('cityborder');
    /*
      Set initial map properties
     */
    function initializeMap() {
        overlay.indeterminate('Initializing map... Please');
        $('input').prop('disabled', true);
        CityBorder.objects.filter({'name': 'Chicago'}, function(data){
            var chicago = data[0];
            var sw = chicago.box.sw;
            var ne = chicago.box.ne;
            map.fitBounds(new google.maps.LatLngBounds(
                {lat:sw.lat, lng:sw.lon}, {lat:ne.lat, lng:ne.lon}));
            var center = JSON.parse(chicago.center).coordinates
            map.setCenter(new google.maps.LatLng(center[1], center[0]));
            map.data.addGeoJson(JSON.parse(chicago.geojson));
            map.data.setStyle({
              strokeWeight: 1
            });
        });
    }
    initializeMap();

    /*
      Bind page actions
     */
    function bindActions() {
      google.maps.event.addDomListener(window, "resize", resizeMap);

      google.maps.event.addListenerOnce(map, 'tilesloaded', function() {
            $('.loading-overlay').remove();
            $('input').prop('disabled', false);
      });
      $('input[type=checkbox].crime-type').on('change', updateCrimeTypes);
      $('input[type=checkbox]#all-types').on('change', toggleAllTypes);
      $('input[type=checkbox].grid-toggle').on('change', toggleGridSizeChoices);
      $('input[type=radio].grid-size').on('change', drawGrid);
      $('#load-crimes').on('click', filterCrimes);
    }
    bindActions();

    /*
      Event handler for making Google Map responsive
     */
    function resizeMap() {
       var center = map.getCenter();
       google.maps.event.trigger(map, "resize");
       map.setCenter(center);
    }

    function toggleGridSizeChoices(){
        if ($(this).is(':checked')){
          $('.grid-sizes').removeClass('hide');
        } else {
          $('.grid-sizes').addClass('hide');
          $('.grid-options input').prop('checked', false);
          for (var i = 0; i < grid.length; i++){
            map.data.remove(grid[i]);
          }
        }
    }

    function drawGrid() {
        $('input').prop('disabled', true);
        for (var i = 0; i < grid.length; i++){
          map.data.remove(grid[i]);
        }
        var pk = 1;
        var size = +$(this).val();
        $.ajax({
            url: '/map/grid',
            type: 'get',
            data: {pk: pk, size: size},
            success: function(response) {
                data = JSON.parse(response);
                grid = map.data.addGeoJson(data);
                visualizeCells(grid);
                $('input').prop('disabled', false);
            }
        })
    }

    function updateCrimeTypes() {
        var type = $(this).val();
        if ($(this).is(':checked')){
          crimeMarkers[type] = [];
          $('#load-crimes').removeClass('disabled');
        } else {
          var markers = crimeMarkers[type];
          for (var j = 0; j< markers.length; j++) {
            var marker = markers[j];
            marker.setMap(null);
          }
          delete crimeMarkers[type];
        }
        var types = Object.keys(crimeMarkers);
        if (types.length === 0) {
            $('#load-crimes').addClass('disabled');
            $('input[type=checkbox]#all-types').prop('checked', false);
            $('input[type=checkbox]#all-types').prop('indeterminate', false);
        } else if (types.length === $('input[type=checkbox].crime-type').length) {
            $('input[type=checkbox]#all-types').prop('checked', true);
            $('input[type=checkbox]#all-types').prop('indeterminate', false);
        } else {
            $('input[type=checkbox]#all-types').prop('checked', false);
            $('input[type=checkbox]#all-types').prop('indeterminate', true);
        }
    }

    function toggleAllTypes(){
        if ($(this).is(':checked')){
            $('input[type=checkbox].crime-type').prop('checked', true);
        } else {
            $('input[type=checkbox].crime-type').prop('checked', false);
        }
        $('input[type=checkbox].crime-type').trigger('change');
    }

    function filterCrimes() {
        var $this = $(this);
        var types = Object.keys(crimeMarkers);
        if (types.length > 0) {
          $('input[type=checkbox]').prop('disabled', true);
          $this.find('i').removeClass('hide');
          $this.addClass('disabled');
          var filters = getCrimeFilters();
          filters['limit'] = 1000;
          Crimes.objects.filter(filters, function(data) {
              for (var i = 0; i < data.length; i++) {
                  var crime = data[i];
                  var lat = crime.latitude;
                  var long = crime.longitude;
                  var marker = new google.maps.Marker({
                      position: new google.maps.LatLng(lat, long),
                      map: map,
                      icon: 'https://maps.gstatic.com/intl/en_us/mapfiles/markers2/measle_blue.png',
                    });
                  var date = new Date(crime.date);
                  crime.date = date.strftime('B d, Y I:Mp');
                  var info = Mustache.render(crimeInfoTemplate, crime);
                  var infowindow = new google.maps.InfoWindow({
                    content: info,
                  });
                  marker.addListener('click', function() {
                    infowindow.open(map, this);
                  });
                  crimeMarkers[crime.primary_type].push(marker);
              }
              $('input[type=checkbox]').prop('disabled', false);
              $this.find('i').addClass('hide');
              $this.removeClass('disabled');
          });
        }
    }

    function getCrimeFilters() {
        var filters = {};
        var types = Object.keys(crimeMarkers);
        if (types.length > 0) {
            filters['primary_type__in'] = types;
        }

        if ($('#start-date').val()) {
            var start = new Date($('#start-date').val());
            var adjusted = new Date(Date.UTC(start.getFullYear(), start.getMonth(), start.getDate()));
            filters['date__gte'] = adjusted.toISOString();
        }

        if ($('#end-date').val()) {
            var end = new Date($('#end-date').val());
            var adjusted = new Date(Date.UTC(end.getFullYear(), end.getMonth(), end.getDate()));
            filters['date__lte'] = adjusted.toISOString();
        }

        if (Object.keys(filters).length > 0) {
          return filters;
        }
        return false;
    }

    function visualizeCells(grid) {
        for (var i = 0; i < grid.length; i++) {
            var cell = grid[i].getGeometry();
            var count = 0;
            poly = new google.maps.Polygon({paths: cell.getAt(0).getArray()});
            for (var key in crimeMarkers) {
                var markers = crimeMarkers[key];
                for (var k = 0; k < markers.length; k++) {
                    var marker = markers[k];
                    if (google.maps.geometry.poly.containsLocation(marker.getPosition(), poly)){
                        count++;
                    }
                }
            }
            grid[i].setProperty('count', count);
            grid[i].setProperty('type', 'cell');
        }
        map.data.setStyle(function(feature){
            if (feature.getProperty('type') === 'cell') {
              var color;
              if (feature.getProperty('count') > 0) {
                color = 'red';
              } else {
                color = 'green';
              }

              return {
                strokeWeight: 1,
                fillColor: color,
              }
            }
        });
    }
});