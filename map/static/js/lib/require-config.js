(function(config) {
    if (window.hasOwnProperty('require')) {
        require.config(config);
    } else {
        window.require = config;
    }
})({
    baseUrl: '/static/js',
    paths: {
        jquery: 'lib/jquery-1.11.3.min',
        async: 'lib/plugins/async',
        goog: 'lib/plugins/goog',
        propertyParser: 'lib/plugins/propertyParser',
        stapes: 'lib/stapes-0.8.1-min',
        hammerjs: 'lib/hammer.min',
        'jquery-hammerjs': 'lib/jquery.hammer',
        materialize: 'materialize.min',
        model: 'model',
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
