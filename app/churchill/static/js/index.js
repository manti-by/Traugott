(function($){

    'use strict';

    $(document).ready(function () {
        // Init shot view
        $.shotView.init();

        // Init shot type view
        $.shotTypeView.init();

        // Handlebars
        $.fn.registerHandlebarHelpers();
    });
})(jQuery);
