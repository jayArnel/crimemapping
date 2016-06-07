require([
    'jquery', 'crimeprediction/js/overlay/overlay', 'hammerjs',
    'jquery-hammerjs', 'materialize',
], function($, overlay) {
    $('.modal-trigger').leanModal();
    $('select').material_select();

    $('#train').on('click', trainModel);
    $('#predict').on('click', predict);

    function trainModel(e){
        e.preventDefault();
        var modal = $('#model-popup');
        overlay.indeterminate('This may take some time... Please Wait.');
        var crimeType = modal.find('select#crime_type').val();
        var grid_size = modal.find('select#grid_size').val();
        var period = modal.find('select#period').val();
        var seasonality = modal.find('.switch#seasonality input').prop('checked')
        console.log(seasonality);
        $.ajax({
            url: '/train',
            type: 'get',
            data: {
                grid_size: grid_size,
                period: period,
                crime_type: crimeType,
                seasonality: seasonality
            },
            success: function() {
                overlay.remove();
            },
        });
    }

    function predict(e){
        e.preventDefault();
        overlay.indeterminate('This may take some time... Please Wait.');
        $.ajax({
            url: '/predict',
            type: 'get',
            data: {},
            success: function() {
                overlay.remove();
            },
        });
    }
});