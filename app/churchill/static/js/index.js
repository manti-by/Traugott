(function($){

    'use strict';

    $(document).ready(function () {
        // Init shot view
        $.shotView.init();

        // Handlebars
        $.fn.registerHandlebarHelpers();

        // @todo: add handlebars renderer for shot types
    });
})(jQuery);
