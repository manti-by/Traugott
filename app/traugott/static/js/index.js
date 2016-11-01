(function($){

    'use strict';

    $(document).ready(function () {

        // Check login state and render appropriate template
        if (window.user && window.user.id) {
            $('#t-shots').render({ cards: window.data }, true);
        } else {
            $('#t-login').render({}, true);
        }

        // Form submissions
        var form = $('form.ajax'),
            error = form.find('.error-holder');

        form.ajaxSubmit(
            function(response) {
                if (response['status'] == 200) {
                    window.user = response['data']['user'];
                    window.data = response['data']['data'];
                    $('#t-shots').render({ cards: window.data }, true);
                } else {
                    error.text(response['message']);
                }
            }, function(xhr) {
                error.text(xhr.statusText);
            }
        );
    });
})(jQuery);
