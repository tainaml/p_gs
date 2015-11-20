require('./when-event.js');

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

        this.init();
    }

    Plugin.prototype.init = function init () {
        var urlCheck = $( this.element ).data( 'urlCheck' ),
            $that = $( this.element );

        $.getJSON(urlCheck, function ( result ) {
            checkResult( $that, result );
        });

        this.activeFavourite();
    };
    Plugin.prototype.activeFavourite = function () {
        var $that = this;

        $( $that.element ).on( 'click.action', function ( event ) {
            var ajaxUrl = event.currentTarget.href;
            event.preventDefault();

            $.getJSON( ajaxUrl, function ( result ) {
                checkResult( $that.element, result );
            });
        });
    };

    function checkResult ( el, result ) {
        var element = $(el);
        result.action = element.data('action');
        console.log(result.acted);
        if ( result.acted ) {
            $('[data-action='+ result.action +'][data-action-type="icon"]').parent('li').addClass( 'item-active' );
            $('[data-action='+ result.action +'][data-action-type="text"]')
                .find('span').text( $('[data-action='+ result.action +'][data-action-type="text"]').data( 'actionTextAlt' ));

        } else {
            $('[data-action='+result.action +'][data-action-type="icon"]').parent('li').removeClass( 'item-active' );
            $('[data-action='+ result.action +'][data-action-type="text"]')
                .find('span').text( $('[data-action='+ result.action +'][data-action-type="text"]').data( 'actionText' ));
            console.log(element.data('actionText'));
        }
    }

    $('[data-action]').on('change:action', function ( event, data ) {
        checkResult(event.currentTarget, data);
    });

    $.fn[pluginName] = function ( options ) {
        return this.each(function () {
            if ( !$.data ( this, 'plugin_' + pluginName )) {
                $.data ( this, 'plugin_' + pluginName,
                new Plugin( this, options ));
            }
        });
    };

    $('[data-action]').ajaxSocialAction();

})(jQuery, window, document);