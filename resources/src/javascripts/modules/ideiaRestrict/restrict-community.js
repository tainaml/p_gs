(function($) {

    $._ideiaRestrictCommunity = function(element, options) {

        var defaultsPrivate = {
            urlCheckLogin   : '/community/check/user-follows/',
            method          : 'post',
            dataType        : 'json',
            modalPosts      : '#modal-alert-community-posts',
            modalQuestions  : '#modal-alert-community-questions'
        };

        var defaults = {
            token: null,
            data : {},

            verify: function( obj, event ) {

                event.preventDefault();

                console.log( 'method verify' );
                console.log( event );

                if ( obj.settings.method == "post" && !obj.settings.token )
                    console.error( 'Token is not defined' );

                if ( obj.settings.token ) {
                    obj.settings.data['csrfmiddlewaretoken'] = obj.settings.token;
                    obj.settings.data['community'] = obj.settings.community;
                    $.ajax({
                        url: obj.settings.urlCheckLogin,
                        method: obj.settings.method,
                        dataType: obj.settings.dataType,
                        data: obj.settings.data,
                        success: function(data) {
                            obj.settings.check( obj, event, data );
                        },
                        error: function(status) {
                            obj.settings.onFailure( obj, event, status );
                        }
                    });
                }

            },

            check: function( obj, event, data ) {
                event.preventDefault();

                console.log(data);

                if ( data.follows == true ) {
                    obj.settings.onSuccessIsFollows( obj, event, data );
                } else {
                    obj.settings.onSuccessIsNotFollows( obj, event, data );
                }
            },

            onSuccessIsFollows: function( obj, event, data ) {
                event.preventDefault();

                console.log( data );
            },

            onSuccessIsNotFollows: function( obj, event, data ) {
                event.preventDefault();

                console.log( data );

                var $modal = (obj.settings.type == "post")
                    ? $(obj.settings.modalPosts)
                    : $(obj.settings.modalQuestions);

                if ( $modal.is( ':hidden' ) )
                    $modal.modal('show');
            },

            onFailure: function( obj, event, status ) {
                event.preventDefault();

                console.log( 'onFailure' );
                console.log( status );
            }

        };

        var plugin = this;
        plugin.settings = {};

        var $element = $(element),
            element = element;

        plugin.init = function() {

            console.log( 'oaksokaos ' );

            plugin.settings = $.extend({}, defaults, options);
            plugin.settings = $.extend({}, plugin.settings, defaultsPrivate);

            $element.on( 'click', function( event ) {
                console.log("No Click");
                plugin.settings.verify( plugin, event );
            });
        };

        plugin.init();

    };

    $.fn.ideiaRestrictCommunity = function(options) {
        return this.each(function() {
            if (undefined == $(this).data('ideiaRestrictCommunity')) {
                var plugin = new $._ideiaRestrictCommunity(this, options);
                $(this).data('ideiaRestrictCommunity', plugin);
            }
        });
    };

    $( document ).on( 'ready', function() {
        $( '[data-restrict=community]' ).each( function () {
            var $e = $( this );
            $e.ideiaRestrictCommunity( $e.data() );
        });
    });

})(jQuery);