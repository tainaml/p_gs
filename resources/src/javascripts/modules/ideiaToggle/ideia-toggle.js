(function($){

    'use strict';

    $.fn.ToggleDisplay = function(data){
        $(this).on("click", function(){
            $($(this).data("selector")).toggle(data);
        });
    };

    function toggleDisplayOnReady(){
        var $links = $('[data-toggle="dropdown"]');
        $links.ToggleDisplay(75);
    }

    $(document).ready(toggleDisplayOnReady);

})(jQuery);