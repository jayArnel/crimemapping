(function(config) {
    if (window.hasOwnProperty('require')) {
        require.config(config);
    } else {
        window.require = config;
    }
})({
    baseUrl: '/static/js/lib',
    paths: {
        jquery: 'jquery-1.11.3.min.js',
        async: 'plugins/async',
    }
});
