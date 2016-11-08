(function($){

    'use strict';

    $(document).ready(function () {
        // Add dialog
        $.fn.initAddDialog();

        // Shot item events
        $.fn.initShotItem();

        // Shots list events
        $.fn.initShotList();

        // Handlebars
        $.fn.registerHandlebarHelpers();
    });
})(jQuery);
