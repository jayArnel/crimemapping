require(['async!https://maps.googleapis.com/maps/api/js?v=3.24&libraries=geometry&sensor=false'], function() {
        /*
      Initialize variables
     */
    var map = new google.maps.Map(document.getElementById('map'));
    var boundariesGeoJSON = 'https://gist.githubusercontent.com/anonymous/0b1f9831d6d4941206f7/raw/b1c4dd632b4466e596169639dcba3bebda693d4e/map.geojson'
    // Chicago City box points
    var NorthEast = new google.maps.LatLng(42.023135, -87.523661);
    var NorthWest = new google.maps.LatLng(42.023135, -87.940101);
    var SouthWest = new google.maps.LatLng(41.644286, -87.940101 );
    var SouthEast = new google.maps.LatLng(41.644286, -87.523661);
    /*
      Set initial map properties
     */
    function initializeMap() {
      var fit = new google.maps.LatLngBounds(SouthEast, NorthEast);
      map.fitBounds(fit);
      map.data.loadGeoJson(boundariesGeoJSON, null, function(feat){
        boundary = feat[0].getGeometry();
        citybounds = new google.maps.Polygon({paths:boundary.getAt(0).getArray()})
        map.data.setStyle(function(feature) {
            var color = 'red';
            var fill = 'gray';
            return /** @type {google.maps.Data.StyleOptions} */({
                fillColor: fill,
                strokeColor: color,
                strokeWeight: 2,
            });
        });
      });
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
});