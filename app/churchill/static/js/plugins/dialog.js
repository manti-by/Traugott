(function($){

    'use strict';

    $.fn.dialog = function(html) {
        var dialog = $('<div class="dialog gradient"></div>');

        dialog.open = function() {
            var width = $(window).width(),
                height = $(window).height();

            if (height < 769) {
                dialog.find('.content').css('width', width).css('height', height - 56);
                dialog.css('height', height).animate({ left: 0 }, 250);
            } else {
                dialog.animate({ opacity: 1 }, 250);
            }
        };

        dialog.close = function() {
            if ($(window).width() < 769) {
                dialog.animate({ left: '100%' }, 250, function () {
                    dialog.remove();
                });
            } else {
                dialog.animate({ opacity: 0 }, 250, function () {
                    dialog.remove();
                });
            }
        };

        dialog.setHtml = function(html) {
            dialog.html(html);
        };

        dialog.html(html);
        dialog.appendTo('body');

        return dialog;
    }

})(jQuery);