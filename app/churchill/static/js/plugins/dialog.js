(function($){

    'use strict';

    $.fn.dialog = function(html) {
        var dialog = $('<div class="dialog gradient"></div>');

        dialog.open = function() {
            if ($(window).width() < 769) {
                dialog.css('height', $(window).height()).animate({ left: 0 }, 250);
            } else {
                dialog.animate({opacity: 1}, 250);
            }
        };

        dialog.close = function() {
            if ($(window).width() < 769) {
                dialog.animate({left: '100%'}, 250, function () {
                    dialog.remove();
                });
            } else {
                dialog.animate({opacity: 0}, 250, function () {
                    dialog.remove();
                });
            }
        };

        dialog.html(html);
        dialog.appendTo('body');

        return dialog;
    }
})(jQuery);