'use strict';

;(function ($) {
    var navLinks = $('.menu-categories > li');

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
