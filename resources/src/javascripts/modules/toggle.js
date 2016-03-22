;( function ($, window, document, undefined) {
    'use strict';

    var $toggleBtn = $('.toggle-box').find('.btn-toggle');

    $toggleBtn.on('click', function (event) {
        var target = $(event.currentTarget).data('target');
        $(target).slideToggle();
    });

}) (jQuery, window, document);