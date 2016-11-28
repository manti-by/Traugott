(function($){

    'use strict';

    $.fn.dialog = function(html) {
        var open = $('.open-dialog'),
            dialog = $('<div class="dialog gradient container"></div>');

        dialog.open = function() {
            open.addClass('hidden');
            dialog.css('height', $(window).height()).animate({ left: 0 }, 250);
        };

        dialog.close = function() {
            open.removeClass('hidden');
            dialog.animate({ left: '100%' }, 250, function() {
                dialog.remove();
            });
        };

        dialog.html(html);
        dialog.prependTo('body');

        return dialog;
    }
})(jQuery);