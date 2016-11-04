(function($){

    'use strict';

    $.fn.initAddDialog = function() {
        var open_button = $('#open-add-shot-dialog'),
            dialog = $('#add-shot-dialog'),
            add_button = dialog.find('.add'),
            close_button = dialog.find('.close'),
            increase_button = dialog.find('.increase'),
            decrease_button = dialog.find('.decrease');

        open_button.on('click', function() {
            dialog.removeClass('hidden');
        });

        add_button.on('click', function() {
            dialog.addClass('hidden');

            var result = [];
            dialog.find('.quantity input').each(function() {
                result.push({
                    type    : parseInt($(this).data('type-id')),
                    quantity: parseInt($(this).val())
                });
            });

            $.ajax({
                url: '/shots/add/',
                type: 'post',
                data: JSON.stringify(result),
                dataType: 'json',
                headers: {
                    'X-CSRFToken': $.fn.getCookie('csrftoken')
                },
                success: function (response) {
                    if (response['status'] == 200) {
                        window.data = response['data'];
                        $('body').trigger('shots:updated');
                    } else {
                        alert(response['message']);
                    }
                },
                error: function(jqXHR) {
                    alert(jqXHR.responseText);
                }
            });
        });

        close_button.on('click', function() {
            dialog.addClass('hidden');
        });

        increase_button.on('click', function() {
            var quantity = $(this).prev('.quantity').find('input'),
                value = parseInt(quantity.val());
            quantity.val(value + 1);
        });

        decrease_button.on('click', function() {
            var quantity = $(this).next('.quantity').find('input'),
                value = parseInt(quantity.val());
            value = value > 0 ? value - 1 : 0;
            quantity.val(value);
        });
    }
})(jQuery);
