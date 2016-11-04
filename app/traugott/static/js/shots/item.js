(function($){

    'use strict';

    $.fn.bindShotItemActions = function() {
        var shot = $(this),
            content = shot.find('.content'),
            actions = shot.find('.actions'),
            delete_button = actions.find('.delete'),
            increase_button = actions.find('.increase'),
            decrease_button = actions.find('.decrease');

        shot.on('updated', function() {
            shot.render('t-shot-item', shot.data());
            shot.bindShotItemActions();
        });

        content.on('click', function () {
            actions.toggleClass('hidden');
        });

        delete_button.on('click', function() {
            var id = $(this).data('id');

            $.ajax({
                url: '/shots/delete/',
                type: 'post',
                data: JSON.stringify({ id: id }),
                dataType: 'json',
                headers: {
                    'X-CSRFToken': $.fn.getCookie('csrftoken')
                },
                success: function (response) {
                    if (response['status'] == 200) {
                        shot.remove();
                    } else {
                        alert(response['message']);
                    }
                },
                error: function(jqXHR) {
                    alert(jqXHR.responseText);
                }
            });
        });

        increase_button.on('click', function() {
            var quantity = $(this).next('.quantity').find('input'),
                value = parseInt(quantity.val());
            quantity.val(value + 1);
        });

        decrease_button.on('click', function() {
            var quantity = $(this).prev('.quantity').find('input'),
                value = parseInt(quantity.val());
            value = value > 0 ? value - 1 : 0;
            quantity.val(value);
        });
    };

    $.fn.initShotItem = function () {
        $('.shot').each(function() {
            $(this).bindShotItemActions();
        });
    };

})(jQuery);
