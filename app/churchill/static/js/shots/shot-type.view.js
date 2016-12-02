(function($){

    'use strict';

    $.shotTypeView = {

        parent_dialog: null,

        init: function(dialog) {
            this.parent_dialog = dialog;
            this.initAddDialog();
        },

        initAddDialog: function() {
            var view = this,
                add_button = $('.add-shot-type'),
                edit_button = $('.edit-my-shots');

            add_button.unbind('click');
            add_button.on('click', function () {
                $.shotIconModel.all({}, function(data) {
                    var html = $.fn.renderTemplate('t-add-shot-type-dialog', { icons: data }, true),
                        add_shot_type_dialog = $.fn.dialog(html);

                    add_shot_type_dialog.open();
                    add_shot_type_dialog.find('.close').on('click', add_shot_type_dialog.close);

                    add_shot_type_dialog.find('.add').on('click', function () {
                        var form = $('#add-shot-type-form'),
                            result =  {
                                title   : form.find('#title').val(),
                                degree  : parseInt(form.find('#degree').val()),
                                volume  : parseInt(form.find('#volume').val()),
                                cost    : parseFloat(form.find('#cost').val().replace(',', '.')),
                                icon    : parseInt(form.find('.icon:checked').val())
                            };

                        $.shotTypeModel.create(result, function (data) {
                            var html = $.fn.renderTemplate('t-add-shot-dialog', data, true);

                            view.parent_dialog.setHtml(html);
                            $.shotView.bindAddDialogActions(view.parent_dialog);

                            add_shot_type_dialog.close();
                        });
                    });

                    // Rebind MLD events
                    componentHandler.upgradeDom();
                });
            });

            edit_button.unbind('click');
            edit_button.on('click', function () {
                $.shotTypeModel.all({}, function (data) {
                    var html = $.fn.renderTemplate('t-edit-my-shots-dialog', { shots: data.user_types }, true),
                        edit_my_shots_dialog = $.fn.dialog(html);

                    edit_my_shots_dialog.open();
                    edit_my_shots_dialog.find('.close').on('click', edit_my_shots_dialog.close);

                    // Rebind MLD events
                    componentHandler.upgradeDom();
                });
            });
        }
    }
})(jQuery);
