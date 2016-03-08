(function(root, declaration) {
    if (typeof define === 'function' && define.amd) {
        define(['stapes', 'jquery'], declaration);
    } else {
        root.Model = declaration(root.Stapes, root.jQuery);
    }
})(this, function(Stapes, $) {

    
    var ModelManager = Stapes.subclass({
        constructor: function(model) {
            this.model = model;
        },
        get: function(pk, callback) {
            if (arguments.length > 1 && typeof arguments[1] !== 'function') {
                throw new Error('Only one primary key is allowed.');
            }
            var url = this.model.baseUrl + pk + '/';
            return this._fetch('GET', url, callback);
        },
        slice: function(start, end, callback) {
            if (arguments.length > 2 && typeof arguments[2] !== 'function') {
                throw new Error('Only two primary keys are allowed.');
            }
            var url = this.model.baseUrl + 'set/' + start + ';' + end + '/';
            return this._fetch('GET', url, callback);
        },
        filter: function(filter, callback) {
            var url = this.model.baseUrl;
            var filterArgs = this._parseGetParams(filter);
            if (filterArgs !== '') {
                url += '?' + filterArgs;
            }

            return this._fetch('GET', url, callback);
        },
        _fetch: function(method, url, callback) {
            return $.ajax({
                url: url,
                type: 'GET',
                success: function(response) {
                    if (typeof callback === 'function') {
                        response = JSON.stringify(response);
                        response = JSON.parse(response);
                        if (response.hasOwnProperty('objects')) {
                            response = response.objects;
                        }
                        callback(response);
                    }
                }
            });
            // $('#results').find('.url').html(url);
            // var req = new XMLHttpRequest();
            // req.open(method, url, true);
            // req.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            // req.onreadystatechange = function() {
            //     if (req.readyState === 4 && req.status === 200 && typeof callback === 'function') {
            //         callback(JSON.parse(req.responseText).object);
            //     }
            // };
            // req.send();
            // return req;
        },
        _parseGetParams: function(params) {
            var query = [];
            for (var key in params) {
                if(params.hasOwnProperty(key)) {
                    query.push(key + '=' + params[key]);
                }
            }
            return query.join('&');
        }
    });

    var Model = Stapes.subclass({
        constructor: function(name) {
            this.baseUrl = '/api/' + name+ '/';
            this.objects = new ModelManager(this);
        },
    });

    return Model;
});
