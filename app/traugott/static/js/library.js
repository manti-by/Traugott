(function($){

    'use strict';

    $.fn.render = function(context) {
        var source   = $(this).html(),
            template = Handlebars.compile(source);
        $('#app').html(template(context));
    };

    $.fn.ajaxSubmit = function (success, error) {
        $(this).on('submit', function(event) {
            event.preventDefault();

            var form = $(this);
            $.ajax({
                url     : form.attr('action'),
                type    : form.attr('method'),
                data    : form.serialize(),
                success : success,
                error   : error
            });

            return false;
        });
    };
})(jQuery);
