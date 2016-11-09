(function($){

    'use strict';

    $.shotView = {

        init: function() {
            var view = this;

            view.initAddDialog();

            $('.shot').each(function(item) {
                view.bindShotItemActions(item);
            });
        },

        initAddDialog: function() {
            var open_button = $('#open-add-shot-dialog'),
                dialog = $('#add-shot-dialog'),
                add_button = dialog.find('.add'),
                close_button = dialog.find('.close'),
                increase_button = dialog.find('.increase'),
                decrease_button = dialog.find('.decrease');

            open_button.on('click', function () {
                dialog.removeClass('hidden');
            });

            add_button.on('click', function () {
                dialog.addClass('hidden');

                var result = [];
                dialog.find('.quantity input').each(function () {
                    result.push({
                        type: parseInt($(this).data('type-id')),
                        quantity: parseInt($(this).val())
                    });
                });

                $.shotModel.add(result, function (data) {
                    $('#shot-list').render('t-shot-list', response['data']);
                });
            });

            close_button.on('click', function () {
                dialog.addClass('hidden');
            });

            increase_button.on('click', function () {
                var quantity = $(this).prev('.quantity').find('input'),
                    value = parseInt(quantity.val());
                quantity.val(value + 1);
            });

            decrease_button.on('click', function () {
                var quantity = $(this).next('.quantity').find('input'),
                    value = parseInt(quantity.val());
                value = value > 0 ? value - 1 : 0;
                quantity.val(value);
            });
        },

        bindShotItemActions: function(shot) {
            var view = this,
                content = shot.find('.content'),
                actions = shot.find('.actions'),
                delete_button = actions.find('.delete'),
                increase_button = actions.find('.increase'),
                decrease_button = actions.find('.decrease');

            content.on('click', function () {
                actions.toggleClass('hidden');
            });

            delete_button.on('click', function() {
                $.shotModel.delete({ id: $(this).data('id') }, shot.remove);
            });

            increase_button.on('click', function() {
                var quantity = $(this).next('.quantity').find('input'),
                    value = parseInt(quantity.val());

                value += 1;
                quantity.val(value);

                view.updateShotQuantity(shot, { id: quantity.data('id'), quantity: value });
            });

            decrease_button.on('click', function() {
                var quantity = $(this).prev('.quantity').find('input'),
                    value = parseInt(quantity.val());

                value = value > 1 ? value - 1 : 1;
                quantity.val(value);

                view.updateShotQuantity(shot, { id: quantity.data('id'), quantity: value });
            });
        },

        updateShotQuantity: function (shot, data) {
            $.shotModel.update(data, function(data) {
                data['opened'] = 1;
                shot.render('t-shot-item', data);
                shot.bindShotItemActions();
            });
        }
    }
})(jQuery);
