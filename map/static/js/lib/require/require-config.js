(function(config) {
    if (window.hasOwnProperty('require')) {
        require.config(config);
    } else {
        window.require = config;
    }
})({
    baseUrl: '/static/js',
    paths: {
        jquery: 'lib/jquery/jquery-1.11.3.min',
        stapes: 'lib/stapes/stapes-0.8.1-min',
        mustache: 'lib/mustache/mustache',
        hammerjs: 'lib/hammer/hammer.min',
        'jquery-hammerjs': 'lib/jquery/jquery.hammer',
        materialize: 'lib/materialize/materialize.min',
        model: 'model/model',
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
