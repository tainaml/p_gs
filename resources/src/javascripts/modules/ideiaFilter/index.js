'use strict';

;(function ($) {
    var $dropdown = $('[data-toggle="dropdown"]');
    var $dropdownText = $dropdown.find('span');
    var $dropdownMenu = $dropdown.siblings('.dropdown-menu');
    var $dropdownMenuListItem = $dropdownMenu.find('li');
    var $dropdownMenuLink = $dropdownMenu.find('a');

    $dropdownMenuLink.on('click', cbDropdownLinkClick);

    function cbDropdownLinkClick (event) {
        event.preventDefault();
        var _this = $(event.currentTarget);
        var url = event.currentTarget.href;
        var text = event.currentTarget.innerHTML;
        var target = event.currentTarget.dataset.target;
        $dropdownMenuListItem.removeClass('active');
        _this.parent('li').addClass('active');
        $dropdownText.text(text);
        filterContent({
            url: url,
            target: target
        });
    }

    function filterContent (options) {
        var defaults = {
            url: '/',
            target: '[data-target="content"]'
        }
        var _options = $.extend({}, defaults, options);
        $(_options.target).empty();
        $.get(_options.url, function (data) {
            $(_options.target).html(data);
        });
    }
})(jQuery);