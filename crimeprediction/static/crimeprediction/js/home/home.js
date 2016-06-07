require([
    'jquery', 'model', 'crimeprediction/js/overlay/overlay', 'hammerjs',
    'jquery-hammerjs', 'materialize',
], function($, Model, overlay) {

    $('.modal-trigger').on('click', populateCityPopup);
    $('#map-popup').on('click', '.city', activateItem);
    $('#map-popup').on('click', '.proceed', linkToMap);

    function populateCityPopup() {
        var popup = $('#map-popup');
        var popupContent = popup.find('.modal-content');
        popupContent.children().slice(1).remove();
        var CityBorder = new Model('cityborder-detail');

        CityBorder.objects.filter({}, function(data) {
            for (var i = 0; i < data.length; i++) {
                var city = data[i];
                var container = $('<div class="col s12 m6"><div class="card-panel city"></div></div>');
                var content = container.find('.card-panel').append($('<span>'+city.name+'</span>'));
                popupContent.append(container);
            }
        });

        popup.openModal();
    }

    function activateItem(e) {
        $(this).closest('#map-popup').find('.city').removeClass('teal');
        $(this).closest('#map-popup').find('.city span').removeClass('white-text');
        $(this).addClass('teal');
        $(this).find('span').addClass('white-text');
        var city = $(this).find('span').text();
        $(this).closest('#map-popup').find('.modal-footer a.proceed').removeClass('disabled');
        $(this).closest('#map-popup').find('.modal-footer a.proceed').attr('href', 'map/'+city);
    }

    function linkToMap(e){
        overlay.indeterminate('Redirecting to map... Please Wait.');
    }

});