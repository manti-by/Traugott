(function($){

    'use strict';

    $(document).ready(function () {

        $('form.ajax').on('submit', function(event) {
            event.preventDefault();

            var form = $(this);
            $.ajax({
                url     : form.attr('action'),
                type    : form.attr('method'),
                data    : form.serialize(),
                success : function(response){
                    if (response['status'] == 200) {
                        location.href = location.href;
                    } else {
                        form.find('.error-holder').text(response['message']);
                    }
                },
                error   : function(xhr) {
                    form.find('.error-holder').text(xhr.statusText);
                }
            });

            return false;
        });
    });
})(jQuery);
