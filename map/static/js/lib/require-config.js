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
        stapes: 'lib/stapes-0.8.1-min',
        model: 'model',
    }
});
