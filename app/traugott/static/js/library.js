(function($){

    'use strict';

    $.fn.render = function(context, update_menu) {
        var source   = $(this).html(),
            template = Handlebars.compile(source),
            html = template(context);
        $('#app').html(html);

        // Update menu
        if (update_menu) {
            source   = $('#t-menu').html();
            template = Handlebars.compile(source);
            html = template({user: window.user});
            $('.menu').each(function() {
                $(this).html(html);
            });
        }
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
