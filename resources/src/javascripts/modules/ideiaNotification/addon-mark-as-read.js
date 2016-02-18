(function($) {

    'use strict';

    $.IdeiaNotificationMarkAsRead = function(element, options) {

        var defaults = {
            target  : null,
            data    : {}

        };

        var plugin = this;
        plugin.settings = {};

        var $element = $( element );

        plugin.init = function() {

            plugin.settings = $.extend({}, defaults, options);

            validate_configs();

            $element.on( 'click', function( event ) {
                event.preventDefault();
                mark_notification_as_read( $( event.currentTarget ) );
            });

        };

        var validate_configs = function( ) {

            var is_valid = true;
            var errors = [];

            if ( !plugin.settings.csrf ) {
                is_valid = false;
                errors.push( 'CSRF is not defined!' );
            }

            if ( !is_valid ) {
                console.error( errors );
            } else {
                if ( plugin.settings.csrf )
                    plugin.settings.data['csrfmiddlewaretoken'] = plugin.settings.csrf;
            }

        };

        var mark_notification_as_read = function( $el ) {

            var url = $el.data( 'next-url' );
            var notification = [];

            notification.push( $el.data( 'notification' ) );

            $.ajax({
                url     : '/notifications/mark-as-read',
                method  : 'post',
                dataType: 'json',
                data    : {
                    notifications: notification,
                    csrfmiddlewaretoken: plugin.settings.data['csrfmiddlewaretoken']
                },
                success : function( data ) {
                    if ( data.status == true ) {
                        window.location.href = url;
                    }
                }
            });

        };

        plugin.init();

    };

    $.fn.IdeiaNotificationMarkAsRead = function( options ) {
        return this.each( function() {
            if ( undefined == $( this ).data( 'IdeiaNotificationMarkAsRead' )) {
                var plugin = new $.IdeiaNotificationMarkAsRead( this, options );
                $( this ).data( 'IdeiaNotificationMarkAsRead', plugin );
            }
        });
    };

    $( document ).on( 'ready', function() {
        $( '[data-trigger=notification-as-read]' ).each( function () {
            var $e = $( this );
            $e.IdeiaNotificationMarkAsRead( $e.data() );
        });
    });

})(jQuery);