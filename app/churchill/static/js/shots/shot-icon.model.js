(function($){

    'use strict';

    $.shotIconModel = {

        _dispatch: function(method, data, success, error) {
            var dispatcher = this;
            $.ajax({
                url: '/shot_icons/',
                type: method,
                data: JSON.stringify(data),
                dataType: 'json',
                headers: {
                    'X-CSRFToken': $.fn.getCookie('csrftoken')
                },
                success: function (response) {
                    if (response.status == 200) {
                        if (success) {
                            success(response.data);
                        } else {
                            dispatcher._success(response.data);
                        }
                    } else {
                        if (error) {
                            error(response.message);
                        } else {
                            dispatcher._error(response.message);
                        }
                    }
                },
                error: function(jqXHR) {
                    if (error) {
                        error(jqXHR.responseText);
                    } else {
                        dispatcher._error(jqXHR.responseText);
                    }
                }
            });
        },

        _success: function(data) {
            console.info(data);
        },

        _error: function(message) {
            $.fn.error(message);
        },

        all: function(data, success, error) {
            this._dispatch('get', data, success, error);
        }
    };
})(jQuery);
