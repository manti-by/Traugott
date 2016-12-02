(function($){

    'use strict';

    $.fn.error = function(message) {
        var html = $.fn.renderTemplate('t-error', { message: message }, true),
            dialog = $(html);

        dialog.appendTo('body');
        $('body, html').on('click', function() {
            dialog.remove();
        });
    };

})(jQuery);