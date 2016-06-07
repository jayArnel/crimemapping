require([
    'jquery', 'hammerjs', 'jquery-hammerjs', 'materialize',
], function($) {
    $('.modal-trigger').leanModal();
    $('select').material_select();
});