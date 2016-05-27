(function($) {

    $._ideiaRestrictCommunity = function(element, options) {

        var $this = $(element);

        var defaultsPrivate = {
            urlCheckLogin   : $this.data("url-check-login"),
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

                if ( obj.settings.method == "post" && !obj.settings.token )
                    console.error( 'Token is not defined' );

                if ( obj.settings.token && $element.data('ideiaRestrictStatus') != 'checking' ) {

                    $element.data('ideiaRestrictStatus', 'checking');

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
                if ( data.follows == true ) {
                    obj.settings.onSuccessIsFollows( obj, event, data );
                } else {
                    obj.settings.onSuccessIsNotFollows( obj, event, data );
                }
            },

            onSuccessIsFollows: function( obj, event, data ) {
                if ( $element.data('ideiaRestrictStatus') != 'checked') {
                    $element.data('ideiaRestrictStatus', 'checked');
                }

                window.location.href = $element.attr('href');
            },

            onSuccessIsNotFollows: function( obj, event, data ) {
                event.preventDefault();

                $element.data('ideiaRestrictStatus', 'checked');

                var $modal = (obj.settings.type == "post")
                    ? $(obj.settings.modalPosts)
                    : $(obj.settings.modalQuestions);

                if ( $modal.is( ':hidden' ) )
                    $modal.modal('show');
            },

            onFailure: function( obj, event, status ) {
                event.preventDefault();
                console.log( 'IdeiaRestrict onFailure' );
            }

        };

        var plugin = this;
        plugin.settings = {};

        var $element = $(element),
            element = element;

        plugin.init = function() {
            plugin.settings = $.extend({}, defaults, options);
            plugin.settings = $.extend({}, plugin.settings, defaultsPrivate);

            $element.on( 'click', function( event ) {
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