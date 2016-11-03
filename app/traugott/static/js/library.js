(function($){

    'use strict';

    $.fn.initAddDialog = function() {
        var open_button = $('#open-add-shot-dialog'),
            dialog = $('#add-shot-dialog'),
            add_button = dialog.find('.add'),
            close_button = dialog.find('.close'),
            increase_button = dialog.find('.increase'),
            decrease_button = dialog.find('.decrease'),
            quantity = dialog.find('.quantity');

        open_button.on('click', function() {
            dialog.removeClass('hidden');
        });

        add_button.on('click', function() {
            dialog.addClass('hidden');
        });

        close_button.on('click', function() {
            dialog.addClass('hidden');
        });

        increase_button.on('click', function() {
            var quantity = $(this).prev('.quantity'),
                value = parseInt(quantity.text());
            quantity.text(value + 1);
        });

        decrease_button.on('click', function() {
            var quantity = $(this).next('.quantity'),
                value = parseInt(quantity.text());
            value = value > 0 ? value - 1 : 0;
            quantity.text(value);
        });

        $.fn.initShotActions = function () {
            $('.shot').each(function() {
                var shot = $(this),
                    content = shot.find('.content'),
                    actions = shot.find('.actions');

                content.on('click', function () {
                    actions.toggleClass('hidden');
                });
            });

        }
    }
})(jQuery);
