(function($) {

    'use strict';

    $.IdeiaNotification = function(element, options) {

        let isInactive = ( false );
        let timeout = 10 * 1000;
        let allowed_notifications = ['members', 'comments', 'notifications'];

        var $document = $( document );
        let page_title = $document.attr( 'title' );

        var defaults = {

            notificationType: null,

            url     : '/notifications/poll/count/[notification_type]',
            method  : 'get',
            dataType: 'json',
            token   : null,
            target  : null,
            data    : {}

        };

        var plugin = this;
        plugin.settings = {};

        var $element = $( element ),
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

                let $target = $(event.currentTarget);
                let $badge = $target.find('.badge');

                $document.attr( 'title', page_title );

                if ($badge.length) {
                    $badge.text('0').hide();
                }

                load_notifications();
                clear_notifications( plugin, event );
            });

        };

        plugin.updateOptions = function( options ) {
            plugin.settings = $.extend({}, plugin.settings, options);
        };

        var updateData = function( options ) {
            plugin.settings = $.extend({}, plugin.settings, options);
        };

        var polling = function( obj ) {
            if ( !isInactive ) {

                if ( polling_is_valid( obj ) ) {

                    if ( !('token' in obj.settings.data) && obj.settings.token )
                        obj.settings.data['token'] = obj.settings.token;

                    $.ajax({
                        url: obj.settings.url.replace('[notification_type]', obj.settings.notificationType),
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

        var polling_is_valid = function( obj ) {

            var is_valid = true;
            var errors = [];

            if ( !obj.settings.notificationType ) {
                is_valid = false;
                errors.push( 'Notification Type is not defined!' );
            }

            if ( $.inArray( obj.settings.notificationType, allowed_notifications ) === -1 ) {
                is_valid = false;
                errors.push( 'Notification Type is not allowed!' );
            }

            if ( !obj.settings.token ) {
                is_valid = false;
                errors.push( 'Token is not defined!' );
            }

            if ( !is_valid ) console.error( errors );

            return is_valid;

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

        var polling_failure = function( obj, jqXHR, textStatus, errorThrown ) {
            console.error( 'polling failure' );
        };

        var load_notifications = function() {

        };

        var clear_notifications = function( obj, event ) {

            var items = $(obj.settings.target).find('ul > li');

            if ( obj.settings.method == "post" && !obj.settings.csrf )
                console.error( 'CSRF is not defined' );

            if ( !('csrfmiddlewaretoken' in obj.settings.data) )
                obj.settings.data['csrfmiddlewaretoken'] = null;

            if ( 'csrfmiddlewaretoken' in obj.settings.data && obj.settings.csrf )
                obj.settings.data['csrfmiddlewaretoken'] = obj.settings.csrf;

            if ( !( 'notifications' in obj.settings.data ) && $element.data( 'notifications' ))
                obj.settings.data['notifications'] = $element.data( 'notifications' );

            $.ajax({
                url     : '/notifications/clear',
                method  : 'post',
                dataType: 'json',
                data    : obj.settings.data,
                success : function( data ) {
                    if ( data.notifications.length > 0 ) {

                        var notifications = $element.data( 'notifications' );

                        console.log( notifications );
                        console.log( $element.data( 'notifications' ) );

                        $.each( data.notifications, function( i, e ) {
                            if ( $.inArray( e, notifications ) ) {
                                var index = notifications.indexOf( e );
                                notifications.splice(index, 1);
                            }
                        });

                        $element.data( 'notifications', notifications );

                        console.log( notifications );
                        console.log( $element.data( 'notifications' ) );
                    }
                }
            });

            setTimeout( function() {

                $.each( items, function( i, e ) {
                    $( e ).removeClass( 'visualized' );
                });

            }, 1500 );

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