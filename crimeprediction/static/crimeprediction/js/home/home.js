require([
    'jquery', 'model', 'hammerjs', 'jquery-hammerjs', 'materialize',
], function($, Model) {

    $('.modal-trigger').on('click', populateCityPopup);

    function populateCityPopup() {
        var popup = $('#map-popup');
        var popupContent = popup.find('.modal-content');
        var CityBorder = new Model('cityborder-detail');

        CityBorder.objects.filter({}, function(data) {
            for (var i = 0; i < data.length; i++) {
                var city = data[i];
                var container = $('<div class="col s12 m6"><div class="card-panel"></div></div>');
                var content = container.find('.card-panel').append($('<span>'+city.name+'</span>'));
                popupContent.append(container);
            }
        });

        popup.openModal();
    }
});