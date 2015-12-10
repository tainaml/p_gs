require('../../vendor/jquery.tinypubsub.js');

;(function ( $, window, document ) {
    'use strict';
    var pluginName = 'ajaxSocialAction',
        defaults = {
            activeClass: 'item-active'
        };

    function Plugin ( element, options ) {
        this.element = element;

        this.options = $.extend( {}, defaults, options );

        this._defaults = defaults;
        this._name = pluginName;

        attachEvents(this.element);
        if (this.element.dataset.urlCheck) {
            $.publish('check/act',
                [this.element, this.element.dataset.urlCheck, this.element.dataset.action]);
        }
    }
    $.subscribe('check/act', checkActHandler);
    $.subscribe('click/act', clickActHandler);

    function checkActHandler (event, element, url, action) {
        $.get(url, function (data) {
            changeStyleButtonCheck[element.dataset.actionType](element.dataset.object, element.dataset.action, data.acted);
        });
    }
    function clickActHandler (event, element, url, dataObject) {
        $.get(url, function (data) {
            $('[data-object='+dataObject+']').each(function (index) {
                changeStyleButtonCheck[$(this).data('actionType')](element.dataset.object, element.dataset.action, data.acted);
            });
        });
    }

    var changeStyleButtonCheck = {
        icon: function (dataObject, action, isActed) {
            var selector = $('[data-object='+dataObject+'][data-action-type=icon]');
            if (isActed) {
                selector.parent('li').addClass(defaults.activeClass);
            } else {
                selector.parent('li').removeClass(defaults.activeClass);
            }
        },
        text: function (dataObject, action, isActed) {
            var selector = $('[data-object='+dataObject+'][data-action-type=text]');
            if (isActed) {
                selector.find('span').text(
                    selector.data('actionTextAlt'))
            } else {
                selector.find('span').text(
                    selector.data('actionText'))
            }
        },
        button: function (dataObject, action, isActed) {
            var selector = $('[data-object='+dataObject+'][data-action-type=button]'),
            toggleClasses = selector.data('className');
            if (isActed) {
                selector.toggleClass(toggleClasses)
                .find('span').text(
                    selector.data('actionTextAlt'))
            } else {
                selector.toggleClass(toggleClasses)
                .find('span').text(
                    selector.data('actionText'))
            }
        }
    };

    function attachEvents (element) {
        var selector = $(element);
        selector.on('click', handlerClick);
    }
    function handlerClick (event) {
        event.preventDefault();

        $.publish('click/act',
            [event.currentTarget, event.currentTarget.href,
                event.currentTarget.dataset.object]);
    }

    $.fn[pluginName] = function ( options ) {
        return this.each(function () {
            if ( !$.data ( this, 'plugin_' + pluginName )) {
                $.data ( this, 'plugin_' + pluginName,
                new Plugin( this, options ));
            }
        });
    };

    $('[data-action]').ajaxSocialAction();
    $(document).on('async.load.success', function (event) {
        $('[data-action]').ajaxSocialAction();
    });

})(jQuery, window, document);