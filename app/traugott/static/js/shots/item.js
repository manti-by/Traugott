(function($){

    'use strict';

    $.fn.bindShotItemActions = function() {
        var shot = $(this),
            content = shot.find('.content'),
            actions = shot.find('.actions'),
            delete_button = actions.find('.delete'),
            increase_button = actions.find('.increase'),
            decrease_button = actions.find('.decrease');

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

            value += 1;
            quantity.val(value);

            $.fn.updateShotQuantity(quantity.data('id'), value, function(data) {
                data['opened'] = 1;
                shot.render('t-shot-item', data);
                shot.bindShotItemActions();
            }, function(error) {
                alert(error);
            });
        });

        decrease_button.on('click', function() {
            var quantity = $(this).prev('.quantity').find('input'),
                value = parseInt(quantity.val());

            value = value > 1 ? value - 1 : 1;
            quantity.val(value);

            $.fn.updateShotQuantity(quantity.data('id'), value, function(data) {
                data['opened'] = 1;
                shot.render('t-shot-item', data);
                shot.bindShotItemActions();
            }, function(error) {
                alert(error);
            });
        });
    };

    $.fn.initShotItem = function () {
        $('.shot').each(function() {
            $(this).bindShotItemActions();
        });
    };

    $.fn.updateShotQuantity = function(id, quantity, success, error) {
        $.ajax({
            url: '/shots/update/',
            type: 'post',
            data: JSON.stringify({ id: id, quantity: quantity }),
            dataType: 'json',
            headers: {
                'X-CSRFToken': $.fn.getCookie('csrftoken')
            },
            success: function (response) {
                if (response['status'] == 200) {
                    success(response['data']);
                } else {
                    error(response['message']);
                }
            },
            error: function(jqXHR) {
                error(jqXHR.responseText);
            }
        });
    };

})(jQuery);
