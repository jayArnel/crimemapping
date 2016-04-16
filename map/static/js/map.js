require([
    'model', 'jquery', 'materialize',
    'goog!maps,3.24,other_params:key=AIzaSyBUGs5RiAn6ao_JS4hV5wCXSIlGZ5qlC1U',
], function(Model, $) {
    $('.datepicker').pickadate({
        onOpen: function() {
          var _this = this.$node;
          if (_this.is('#start-date')) {
              this.set('max', new Date($('.datepicker#end-date').val()));
          } else if (_this.is('#end-date')) {
              this.set('min', new Date($('.datepicker#start-date').val()));
          }
        },
        onClose: function() {
            $(document.activeElement).blur();
        },
        onStart: function() {
          var initial = this.$node.data('initial');
          this.set('select', new Date(initial));
        },
        min: new Date($('.datepicker#start-date').data('initial')),
        max: new Date($('.datepicker#end-date').data('initial')),
        selectYears: 20,
        selectMonths: true,
    });
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

    // // Chicago City box points
    var NorthEast = new google.maps.LatLng(42.023135, -87.523661);
    var NorthWest = new google.maps.LatLng(42.023135, -87.940101);
    var SouthWest = new google.maps.LatLng(41.644286, -87.940101);
    var SouthEast = new google.maps.LatLng(41.644286, -87.523661);
    var Crimes = new Model('criminalrecord');
    var CityBorder = new Model('cityborder');
    /*
      Set initial map properties
     */
    function initializeMap() {
        CityBorder.objects.filter({'name': 'Chicago'}, function(data){
            var chicago = data[0];
            var sw = chicago.box.sw;
            var ne = chicago.box.ne;
            map.fitBounds(new google.maps.LatLngBounds(
                {lat:sw.lat, lng:sw.lon}, {lat:ne.lat, lng:ne.lon}));
            var center = JSON.parse(chicago.center).coordinates
            map.setCenter(new google.maps.LatLng(center[1], center[0]));
            feat = map.data.addGeoJson(JSON.parse(chicago.geojson));
            boundary = feat[0].getGeometry();
            var citybounds = new google.maps.Polygon({paths:boundary.getAt(0).getAt(0).getArray()});
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
      });

      $('input[type=checkbox].crime-type').on('change', updateCrimeTypes);
      $('input[type=checkbox].grid-toggle').on('change', toggleGridSizeChoices);
      $('input[type=radio].grid-size').on('change', drawGrid);
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
            url: '/grid',
            type: 'get',
            data: {pk: pk, size: size},
            success: function(response) {
                data = JSON.parse(response);
                grid = map.data.addGeoJson(data);
                $('input').prop('disabled', false);
            }
        })
    }

    function updateCrimeTypes() {
        var type = $(this).val();
        if ($(this).is(':checked')){
          crimeMarkers[type] = [];
        } else {
          var markers = crimeMarkers[type];
          for (var j = 0; j< markers.length; j++) {
            var marker = markers[j];
            marker.setMap(null);
          }
          delete crimeMarkers[type];
        }
        filterCrimes();
    }

    function filterCrimes() {
        var types = Object.keys(crimeMarkers);
        if (types.length > 0) {
          $('input[type=checkbox]').prop('disabled', true);
          Crimes.objects.filter({primary_type__in: types}, function(data) {
              for (var i = 0; i < data.length; i++) {
                  var crime = data[i];
                  var lat = crime.latitude;
                  var long = crime.longitude;
                  var marker = new google.maps.Marker({
                      position: new google.maps.LatLng(lat, long),
                      map: map,
                      icon: 'https://maps.gstatic.com/intl/en_us/mapfiles/markers2/measle_blue.png',
                    });
                  crimeMarkers[crime.primary_type].push(marker);
              }
              $('input[type=checkbox]').prop('disabled', false);
          });
        }
    }
});