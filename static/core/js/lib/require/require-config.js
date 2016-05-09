(function(config) {
    if (window.hasOwnProperty('require')) {
        require.config(config);
    } else {
        window.require = config;
    }
})({
    baseUrl: '/static/',
    paths: {
        jquery: 'core/js/lib/jquery/jquery-1.11.3.min',
        stapes: 'core/js/lib/stapes/stapes-0.8.1-min',
        mustache: 'core/js/lib/mustache/mustache',
        hammerjs: 'core/js/lib/hammer/hammer.min',
        'jquery-hammerjs': 'core/js/lib/jquery/jquery.hammer',
        materialize: 'core/js/lib/materialize/materialize.min',
        model: 'core/js/model/model',
        strftime: 'core/js/strftime/strftime',
        gmaps: 'https://maps.googleapis.com/maps/api/js?key=AIzaSyBUGs5RiAn6ao_JS4hV5wCXSIlGZ5qlC1U',
    },
    shim: {
        materialize: {
            deps: ['jquery', 'hammerjs', 'jquery-hammerjs'],
        },
        jquery: {
            exports: '$'
        }
    }
});
