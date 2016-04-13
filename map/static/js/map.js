require([
    'model', 'jquery', 'materialize',
    'goog!maps,3.24,other_params:key=AIzaSyBUGs5RiAn6ao_JS4hV5wCXSIlGZ5qlC1U',
], function(Model, $) {
    /*
      Initialize variables
     */
    var map = new google.maps.Map(document.getElementById('map'), {
        mapTypeControlOptions: {
            position: google.maps.ControlPosition.TOP_RIGHT,
        }
    });

    // // Chicago City box points
    var NorthEast = new google.maps.LatLng(42.023135, -87.523661);
    var NorthWest = new google.maps.LatLng(42.023135, -87.940101);
    var SouthWest = new google.maps.LatLng(41.644286, -87.940101);
    var SouthEast = new google.maps.LatLng(41.644286, -87.523661);
    var Crimes = new Model('crime');
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
        Crimes.objects.filter({}, function (data){
            for (var i = 0; i < data.length; i++) {
                var crime = data[i];
                var lat = crime.latitude;
                var long = crime.longitude;
                new google.maps.Marker({
                    position: new google.maps.LatLng(lat, long),
                    map: map,
                    icon: 'https://maps.gstatic.com/intl/en_us/mapfiles/markers2/measle_blue.png',
                  });
            }
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

    function drawGrid(pk, size) {
        $.ajax({
            url: '/grid',
            type: 'get',
            data: {pk: pk, size: size},
            success: function(response) {
                console.log(response);
                data = JSON.parse(response);
                map.data.addGeoJson(data);
            }
        })
    }
});