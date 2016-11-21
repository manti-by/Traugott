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
            var view = this;

            $('.add-shot').on('click', function () {
                $.shotTypeModel.all({}, function(data) {
                    var html = $.fn.renderTemplate('t-add-shot-dialog', data, true),
                        add_shot_dialog = $.fn.dialog(html);

                    add_shot_dialog.open();

                    add_shot_dialog.find('.close').on('click', add_shot_dialog.close);

                    add_shot_dialog.find('.add').on('click', function () {
                        var result = [];
                        add_shot_dialog.find('.quantity input').each(function () {
                            if ($(this).val() > 0) {
                                result.push({
                                    type    : parseInt($(this).data('type-id')),
                                    quantity: parseInt($(this).val())
                                });
                            }
                        });

                        $.shotModel.create(result, function (data) {
                            $('#shot-list').renderTemplate('t-shot-list', data);
                            $.each($('.shot'), function() {
                                view.bindShotItemActions($(this));
                            });
                            add_shot_dialog.close();
                        });
                    });

                    add_shot_dialog.find('.increase').on('click', function () {
                        var quantity = $(this).prev('.quantity').find('input'),
                            value = parseInt(quantity.val());
                        quantity.val(value + 1);
                    });

                    add_shot_dialog.find('.decrease').on('click', function () {
                        var quantity = $(this).next('.quantity').find('input'),
                            value = parseInt(quantity.val());
                        value = value > 0 ? value - 1 : 0;
                        quantity.val(value);
                    });

                    // Rebind MLD events
                    componentHandler.upgradeElement(
                        document.getElementById('shot-type-button'),
                        'MaterialButton'
                    );
                    componentHandler.upgradeElement(
                        document.getElementById('shot-type-menu'),
                        'MaterialMenu'
                    );
                    componentHandler.upgradeElement(
                        document.getElementById('shot-type-tabs'),
                        'MaterialTabs'
                    );
                });
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
