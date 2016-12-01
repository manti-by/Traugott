(function($){

    'use strict';

    $.shotView = {

        init: function() {
            var view = this;

            view.initAddDialog();
            view.initShotList();
        },

        initShotList: function() {
            var view = this;

            $.shotModel.all({}, function (data) {
                $('#shot-list').renderTemplate('t-shot-list', { shots: data });
                $.each($('.shot'), function() {
                    view.bindShotItemActions($(this));
                });
            });
        },

        initAddDialog: function() {
            var view = this;

            $('.add-shot').on('click', function () {
                $.shotTypeModel.all({}, function (data) {
                    var html = $.fn.renderTemplate('t-add-shot-dialog', data, true),
                        dialog = $.fn.dialog(html);

                    view.bindAddDialogActions(dialog);
                    dialog.open();
                });
            });
        },

        bindAddDialogActions: function(dialog) {
            var view = this;

            dialog.find('.close').on('click', dialog.close);

            dialog.find('.add').on('click', function () {
                var result = [];
                dialog.find('.mdl-tabs__panel.is-active')
                    .find('.volume input').each(function () {
                        if ($(this).val() > 0) {
                            result.push({
                                type    : parseInt($(this).data('type-id')),
                                volume  : parseInt($(this).val())
                            });
                        }
                });

                $.shotModel.create(result, function (data) {
                    $('#shot-list').renderTemplate('t-shot-list', data);
                    $.each($('.shot'), function() {
                        view.bindShotItemActions($(this));
                    });
                    dialog.close();
                });
            });

            dialog.find('.increase').on('click', function () {
                var volume = $(this).prev('.volume').find('input'),
                    value = parseInt(volume.val()),
                    step = parseInt(volume.data('step'));

                volume.val(value + step);
            });

            dialog.find('.decrease').on('click', function () {
                var volume = $(this).next('.volume').find('input'),
                    nullable = !$(this).next('.volume').hasClass('non-nullable'),
                    value = parseInt(volume.val()),
                    step = parseInt(volume.data('step'));

                value = value - step > 0 ? value - step :
                    nullable ? 0 : value;
                volume.val(value);
            });

            // Bind shot type actions
            $.shotTypeView.init(dialog);

            // Rebind MLD events
            componentHandler.upgradeDom();
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
                var volume = $(this).next('.volume').find('input'),
                    value = parseInt(volume.val()),
                    step = parseInt(volume.data('step'));

                value = value + step;
                volume.val(value);

                view.updateShotVolume(shot, { id: volume.data('type-id'), volume: value });
            });

            decrease_button.unbind('click');
            decrease_button.on('click', function() {
                var volume = $(this).prev('.volume').find('input'),
                    value = parseInt(volume.val()),
                    step = parseInt(volume.data('step'));

                value = value - step > 0 ? value - step : value;
                volume.val(value);

                view.updateShotVolume(shot, { id: volume.data('type-id'), volume: value });
            });
        },

        updateShotVolume: function (shot, data) {
            var view = this;

            $.shotModel.update(data, function(data) {
                data['opened'] = 1;
                shot.renderTemplate('t-shot-item', data);
                view.bindShotItemActions(shot);
            });
        }
    }
})(jQuery);
