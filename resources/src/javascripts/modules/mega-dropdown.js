'use strict';

;(function ($) {
    var navLinks = $('.menu-categories > li');
    // navLinks.on({
    //     'mouseenter': showMenu,
    //     'mouseleave': function (event) {
    //         var $menuArea = $(this).find('.menu-area');
    //         event.preventDefault();
    //         console.log('Mouse event type: %s', event.type);

    //         $menuArea.slideUp('fast');
    //         // return false;
    //     }
    // });

    function showMenu (event) {
        event.preventDefault();
        event.stopPropagation();
        console.log('Mouse event type: %s', event.type);
        var target = $(event.currentTarget).find('.menu-area');
        // $('.menu-area').slideUp('fast');
        $(target).slideDown();
        // return false;
    }

    var delay = 300, setTimeoutConst,
        delay2 = 100, setTimeoutConst2;
    navLinks.mouseover(function(event) {
        var target = $(event.currentTarget).find('.menu-area');
        setTimeoutConst = setTimeout(function(){
            target.slideDown();
        }, delay);
    }).mouseout(function (event) {
        var target = $(event.currentTarget).find('.menu-area');
        clearTimeout(setTimeoutConst );
        setTimeoutConst2 = setTimeout(function(){
            var isHover = target.is(':hover');
            if ( isHover !== true ) {
                target.hide();
            }
        }, delay2);
    });
})(jQuery);
