(function(root, library) {
    if (typeof define === 'function' && define.amd) {
        define([
            'jquery', 'text!crimeprediction/mustachetemplates/map/overlay.html'
        ], library);
    } else {
        root.ThreadComments = library(root.jQuery);
    }

})(this, function($, overlayTemplate) {

    var overlay = $(overlayTemplate);

    function showIndeterminate(message) {
        $('body').append(overlay);
        overlay.find('#progress-bar').addClass('indeterminate');
        overlay.find('#progress-message').text(message);
    }

    function remove() {
        overlay.remove();
    }


    return {
        indeterminate: showIndeterminate,
        remove: remove,
    };

});