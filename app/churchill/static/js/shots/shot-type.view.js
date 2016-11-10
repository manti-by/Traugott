(function($){

    'use strict';

    $.shotTypeView = {

        init: function() {
            var view = this;

            view.initAddDialog();
        },

        initAddDialog: function() {
            var open_button = $('#open-add-shot-type-dialog'),
                add_shot_dialog = $('#add-shot-dialog'),
                add_shot_type_dialog = $('#add-shot-type-dialog'),
                add_button = add_shot_type_dialog.find('.add'),
                close_button = add_shot_type_dialog.find('.close');

            open_button.on('click', function () {
                add_shot_dialog.addClass('hidden');
                add_shot_type_dialog.removeClass('hidden');
            });

            add_button.on('click', function () {
                var result = {
                    title: add_shot_type_dialog.find('#title').val(),
                    volume: parseInt(add_shot_type_dialog.find('#volume').val()),
                    degree: parseInt(add_shot_type_dialog.find('#degree').val())
                };

                $.shotTypeModel.create(result, function (data) {
                    $('#add-shot-dialog').renderTemplate('t-add-shot-dialog', data);

                    add_shot_dialog.removeClass('hidden');
                    add_shot_type_dialog.addClass('hidden');
                });
            });

            close_button.on('click', function () {
                add_shot_type_dialog.addClass('hidden');
            });
        }
    }
})(jQuery);
