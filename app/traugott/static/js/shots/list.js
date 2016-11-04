(function($) {

    'use strict';

    $.fn.initShotList = function () {
        $('body').on('shots:updated', function () {
            location.reload();
        });
    };

})(jQuery);