(function($) {

    'use strict';

    $.IdeiaNotification = function(element, options) {

        let isInactive = ( false );
        let timeout = 5000;

        var defaults = {

            url     : '/notification/poll/[notification_type]',
            method  : 'get',
            dataType: 'json',
            token   : null,
            data    : {}

        };

        var plugin = this;
        plugin.settings = {};

        var $element = $(element),
            element = element;

        plugin.init = function() {

            plugin.settings = $.extend({}, defaults, options);

            setInterval( function() {
                polling( plugin );
            } , timeout );


            $( window ).on( 'focus', function() {
                isInactive = ( false );
            });

            $( window ).on( 'blur', function() {
                isInactive = ( true );
            });

            $element.on( 'click', function( event ) {
                event.preventDefault();
                console.log( event );
            });

        };

        plugin.foo_public_method = function() {};
        plugin.updateData = function() {
            plugin.settings = $.extend({}, plugin.settings, options);
        };

        var polling = function( obj ) {
            if ( !isInactive ) {

                if ( !obj.settings.token )
                    console.error( 'Token is not defined' );

                if ( !('token' in obj.settings.data) )
                    obj.settings.data['token'] = null;

                if ( !('token' in obj.settings.data) && obj.settings.token )
                    obj.settings.data['token'] = obj.settings.token;

                $.ajax({
                    url: obj.settings.url.replace('[notification_type]', obj.settings.notificationType),
                    method: obj.settings.method,
                    dataType: obj.settings.dataType,
                    data: obj.settings.data,
                    success: function(data) {
                        polling_success( obj, data );
                    },
                    error: function(status) {
                        polling_failure( obj, status );
                    }
                });

            }
        };

        var polling_success = function( obj, data ) {

        };

        var polling_failure = function( obj, data ) {

        };

        plugin.init();

    };

    $.fn.IdeiaNotification = function( options ) {
        return this.each( function() {
            if ( undefined == $( this ).data( 'IdeiaNotification' )) {
                var plugin = new $.IdeiaNotification( this, options );
                $( this ).data( 'IdeiaNotification', plugin );
            }
        });
    };

    $( document ).on( 'ready', function() {
        $( '[data-trigger=notification]' ).each( function () {
            var $e = $( this );
            $e.IdeiaNotification( $e.data() );
        });
    });

})(jQuery);