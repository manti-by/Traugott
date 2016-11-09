(function($){

    'use strict';

    $.fn.getCookie = function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    $.fn.registerHandlebarHelpers = function() {
        Handlebars.registerPartial('shot-item', function(data) {
            var source = $('#t-shot-item').html(),
                template = Handlebars.compile(source);
            return template(data);
        });
        Handlebars.registerPartial('shot-type-item', function(data) {
            var source = $('#t-shot-type-item').html(),
                template = Handlebars.compile(source);
            return template(data);
        });
    };

    $.fn.render = function(template_name, data) {
        var source   = $('#' + template_name).html(),
            template = Handlebars.compile(source);
        $(this).html(template(data));
    };

})(jQuery);
