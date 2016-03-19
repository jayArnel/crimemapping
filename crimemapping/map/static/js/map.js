require([
    'model',
    'async!https://maps.googleapis.com/maps/api/js?v=3.24&libraries=geometry&sensor=false'
], function(Model) {
    /*
      Initialize variables
     */
    var map = new google.maps.Map(document.getElementById('map'));

    // // Chicago City box points
    var NorthEast = new google.maps.LatLng(42.023135, -87.523661);
    var NorthWest = new google.maps.LatLng(42.023135, -87.940101);
    var SouthWest = new google.maps.LatLng(41.644286, -87.940101 );
    var SouthEast = new google.maps.LatLng(41.644286, -87.523661);
    var Crimes = new Model('crime');
    var CityBorder = new Model('cityborder');
    /*
      Set initial map properties
     */
    function initializeMap() {
        CityBorder.objects.filter({'name': 'Chicago'}, function(data){
            var chicago = data[0];
            var sw = chicago.bounds.sw;
            var ne = chicago.bounds.ne;
            map.fitBounds(new google.maps.LatLngBounds(
                {lat:sw[0], lng:sw[1]}, {lat:ne[0], lng:ne[1]}));
            var center = JSON.parse(chicago.center).coordinates
            map.setCenter(new google.maps.LatLng(center[1], center[0]));
            var feat = map.data.addGeoJson(JSON.parse(chicago.geojson))[0]; 
        })
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
        // drawGrid();
    }
    initializeMap();

    /*
      Bind page actions
     */
    function bindActions() {
      google.maps.event.addDomListener(window, "resize", resizeMap);
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

    function drawGrid() {
        var rect_number = 0;
        var distance = grid_size;  // grid size distance, you can change this value from grid_size (in meters)
        var dist_coords_long = google.maps.geometry.spherical.computeOffset(NorthWest, distance, 90);
        dist_coords_long = dist_coords_long.lng() - NorthWest.lng();
        var dist_coords_lat = google.maps.geometry.spherical.computeOffset(NorthWest, distance, 180);
        dist_coords_lat = NorthWest.lat() - dist_coords_lat.lat();

        var NW = google.maps.geometry.spherical.computeOffset(NorthWest, distance, 270);

        // check if current square is has not reached the southwest border.
        while(NW.lat() >= SouthWest.lat()) {
            curr_NE = new google.maps.LatLng(NW.lat(), NW.lng() + dist_coords_long);
            curr_SW = new google.maps.LatLng(NW.lat() - dist_coords_lat, NW.lng());
            curr_NW = NW;
            NW = new google.maps.LatLng(NW.lat() - dist_coords_lat, NW.lng());
            // check if current square has not reached the northeast border
            while(curr_NW.lng() <= NorthEast.lng()) {
                // create new southwest and northeast coordnates for a new square
                NE = new google.maps.LatLng(curr_NE.lat(), curr_NE.lng() + dist_coords_long);
                SW = new google.maps.LatLng(curr_SW.lat(), curr_SW.lng() + dist_coords_long);
                // save current square coordinates
                curr_NW = NE;
                curr_NE = NE;
                curr_SW = SW;

                // create bounds from southwest and northeast coordinates
                var bounds = new google.maps.LatLngBounds(SW,NE)
                var bound_NW = new google.maps.LatLng(NE.lat(),SW.lng());
                var bound_SE = new google.maps.LatLng(SW.lat(), NE.lng());

                //check if any of the new bounds vertices is within the city bounds
                if (google.maps.geometry.poly.containsLocation(bound_NW, citybounds) || 
                    google.maps.geometry.poly.containsLocation(NE, citybounds) || 
                    google.maps.geometry.poly.containsLocation(SW, citybounds) || 
                    google.maps.geometry.poly.containsLocation(bound_SE, citybounds)){

                    var rectangle = new google.maps.Rectangle();
                    var rectOptions = {
                        strokeColor: "gray",
                        strokeOpacity: 0.8,
                        strokeWeight: 2,
                        fillOpacity: 0,
                        map: map,
                        bounds: bounds,
                        counts: 0,
                        number: rect_number,
                        merged: false,
                    };
                    rectangle.setOptions(rectOptions);
                    rectangle.getBounds().extend(bound_NW);
                    rectangle.getBounds().extend(bound_SE);
                    rectArr.push(rectangle);
                }
            }
        }
    }

});