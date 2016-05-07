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
        async: 'lib/require/plugins/async',
        goog: 'lib/require/plugins/goog',
        propertyParser: 'lib/require/plugins/propertyParser',
        stapes: 'lib/stapes/stapes-0.8.1-min',
        hammerjs: 'lib/hammer/hammer.min',
        'jquery-hammerjs': 'lib/jquery/jquery.hammer',
        materialize: 'lib/materialize/materialize.min',
        model: 'model/model',
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
