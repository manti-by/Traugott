(function($){

    'use strict';

    $.shotTypeView = {

        init: function() {
            var view = this;

            view.initAddDialog();
        },

        initAddDialog: function() {
            var open_button = $('.add-shot-type');

            open_button.unbind('click');
            open_button.on('click', function () {
                $.shotTypeModel.all({}, function(data) {
                    var html = $.fn.renderTemplate('t-add-shot-type-dialog', data, true),
                        add_shot_type_dialog = $.fn.dialog(html);

                    add_shot_type_dialog.open();
                    add_shot_type_dialog.find('.close').on('click', add_shot_type_dialog.close);

                    add_shot_type_dialog.find('.add').on('click', function () {
                        add_shot_type_dialog.close();
                    });
                });
            });
        }
    }
})(jQuery);
