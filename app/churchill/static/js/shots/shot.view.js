(function($){

    'use strict';

    $.shotView = {

        init: function() {
            var view = this;

            view.initAddDialog();

            $.each($('.shot'), function() {
                view.bindShotItemActions($(this));
            });
        },

        initAddDialog: function() {
            var view = this,
                open_button = $('#open-add-shot-dialog'),
                add_shot_dialog = $('#add-shot-dialog'),
                add_button = add_shot_dialog.find('.add'),
                close_button = add_shot_dialog.find('.close'),
                increase_button = add_shot_dialog.find('.increase'),
                decrease_button = add_shot_dialog.find('.decrease');

            open_button.unbind('click');
            open_button.on('click', function () {
                add_shot_dialog.removeClass('hidden');
            });

            add_button.unbind('click');
            add_button.on('click', function () {
                add_shot_dialog.addClass('hidden');

                var result = [];
                add_shot_dialog.find('.quantity input').each(function () {
                    if ($(this).val() > 0) {
                        result.push({
                            type: parseInt($(this).data('type-id')),
                            quantity: parseInt($(this).val())
                        });
                    }
                });

                $.shotModel.create(result, function (data) {
                    $('#shot-list').renderTemplate('t-shot-list', data);
                    $.each($('.shot'), function() {
                        view.bindShotItemActions($(this));
                    });
                });
            });

            close_button.unbind('click');
            close_button.on('click', function () {
                add_shot_dialog.addClass('hidden');
            });

            increase_button.unbind('click');
            increase_button.on('click', function () {
                var quantity = $(this).prev('.quantity').find('input'),
                    value = parseInt(quantity.val());
                quantity.val(value + 1);
            });

            decrease_button.unbind('click');
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

            content.unbind('click');
            content.on('click', function () {
                actions.toggleClass('hidden');
            });

            delete_button.unbind('click');
            delete_button.on('click', function() {
                $.shotModel.remove({ id: $(this).data('id') }, function() {
                    shot.remove();
                });
            });

            increase_button.unbind('click');
            increase_button.on('click', function() {
                var quantity = $(this).next('.quantity').find('input'),
                    value = parseInt(quantity.val());

                value += 1;
                quantity.val(value);

                view.updateShotQuantity(shot, { id: quantity.data('id'), quantity: value });
            });

            decrease_button.unbind('click');
            decrease_button.on('click', function() {
                var quantity = $(this).prev('.quantity').find('input'),
                    value = parseInt(quantity.val());

                value = value > 1 ? value - 1 : 1;
                quantity.val(value);

                view.updateShotQuantity(shot, { id: quantity.data('id'), quantity: value });
            });
        },

        updateShotQuantity: function (shot, data) {
            var self = this;
            $.shotModel.update(data, function(data) {
                data['opened'] = 1;
                shot.renderTemplate('t-shot-item', data);
            });
        }
    }
})(jQuery);
