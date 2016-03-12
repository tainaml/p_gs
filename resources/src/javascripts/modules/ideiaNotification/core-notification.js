(function($) {

    'use strict';

    $.IdeiaNotification = function(element, options) {

        let isInactive = ( false );
        let timeout = 10 * 1000;
        let allowed_notifications = ['members', 'posts', 'general'];

        var $document = $( document );
        let page_title = $document.attr( 'title' );

        var $element = $( element );

        var defaults = {

            // '/notifications/poll/count/[notification_type]'
            urlCount: $element.data("url-count"),
            // '/notifications/poll/load/[notification_type]'
            urlLoad : $element.data("url-load"),
            method  : 'get',
            dataType: 'json',
            token   : null,
            target  : null,
            csrf    : null,
            data    : {}

        };

        var plugin = this;
        plugin.settings = {};
        plugin.init = function() {

            plugin.settings = $.extend({}, defaults, options);

            validate_configs( plugin );

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

                let $target = $( event.currentTarget );
                let $badge = $target.find('.badge');

                if ( $target.data( 'notifications').length > 0 ) {
                    $document.attr( 'title', page_title );
                }

                if ($badge.length) {
                    $badge.text('0').hide();
                }

                load_notifications( plugin );

                setTimeout( function() {
                    clear_notifications( plugin );
                }, 500 );
            });

        };

        var validate_configs = function( obj ) {

            var is_valid = true;
            var errors = [];


            if ( !obj.settings.token ) {
                is_valid = false;
                errors.push( 'Token is not defined!' );
            }

            if ( obj.settings.method == "post" && !obj.settings.csrf ) {
                is_valid = false;
                errors.push( 'CSRF is not defined!' );
            }

            if ( !is_valid ) {
                console.error( errors );
            } else {
                if ( obj.settings.csrf )
                    obj.settings.data['csrfmiddlewaretoken'] = obj.settings.csrf;

                if ( obj.settings.token )
                    obj.settings.data['token'] = obj.settings.token;
            }


            return false
        };

        var polling_is_valid = function( obj ) {

            var is_valid = true;
            var errors = [];


            if ( !obj.settings.token ) {
                is_valid = false;
                errors.push( 'Token is not defined!' );
            }

            if ( !is_valid ) console.error( errors );

            return is_valid;

        };

        var polling = function( obj ) {
            if ( !isInactive ) {

                if ( polling_is_valid( obj ) ) {

                    if ( !('token' in obj.settings.data) && obj.settings.token )
                        obj.settings.data['token'] = obj.settings.token;

                    $.ajax({
                        url: obj.settings.urlCount,
                        method: obj.settings.method,
                        dataType: obj.settings.dataType,
                        data: obj.settings.data,
                        success: function( data, textStatus, jqXHR ) {
                            polling_success( obj, data, textStatus, jqXHR );
                        },
                        error: function( jqXHR, textStatus, errorThrown ) {
                            polling_failure( obj, jqXHR, textStatus, errorThrown );
                        }
                    });

                }

            }
        };

        var polling_success = function( obj, data ) {

            var $badge = $element.find( 'span.badge' );

            if ( data.count > 0 ) {
                $document.attr( 'title', page_title + ' | Novas notificações');
            }

            $element.data( 'notifications', data.notifications );

            if ( !$badge.length ) {

                if ( data.count > 0 ) {

                    var $newBadge = $( '<span/>' );
                    $newBadge
                        .addClass( 'badge' )
                        .text( data.count );

                    $element.prepend( $newBadge );
                }

            } else {

                $badge.text( data.count );

                if ( data.count == 0 )
                    $badge.text('0').hide();
                else
                    if ( $badge.is( ':hidden' ))
                        $badge.show();

            }
        };

        var polling_failure = function( obj, jqXHR, textStatus, errorThrown ) {};

        var load_notifications = function( obj ) {

            var $notificationsContainer = $( obj.settings.target );
            var notifications = $element.data( 'notifications' ) || [];

            obj.settings.data['notifications'] = notifications;

            if ( notifications.length > 0 ) {
                $.ajax({
                    url     : obj.settings.urlLoad,
                    method  : 'get',
                    dataType: 'json',
                    data    : obj.settings.data,
                    success : function( data ) {
                        if ( data.notifications.length > 0 ) {
                            $notificationsContainer.html( data.template );
                            $element.data( 'notifications', notifications );

                            $( '[data-trigger=notification-as-read]' ).each( function () {
                                var $e = $( this );
                                $e.IdeiaNotificationMarkAsRead( $e.data() );
                            });
                        }
                    }
                });
            }
        };

        var clear_notifications = function( obj ) {

            var notifications = $element.data( 'notifications' ) || [];

            obj.settings.data['notifications'] = notifications;
            if ( notifications.length > 0 ) {
                $.ajax({
                    url     : obj.settings.urlClear,
                    method  : 'post',
                    dataType: 'json',
                    data    : obj.settings.data,
                    success : function( data ) {
                        if ( data.notifications.length > 0 ) {

                            $.each( data.notifications, function( i, e ) {
                                if ( $.inArray( e, notifications ) !== -1 ) {
                                    var index = notifications.indexOf( e );
                                    notifications.splice(index, 1);
                                }
                            });

                            $element.data( 'notifications', notifications );
                        }
                    }
                });
            }
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