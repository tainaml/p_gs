// jQuery Plugin Boilerplate
// A boilerplate for jumpstarting jQuery plugins development
// version 1.1, May 14th, 2011
// by Stefan Gabos

// remember to change every instance of "ideiaLogin" to the name of your plugin!
(function($) {

    // here we go!
    $.ideiaLogin = function(element, options) {

        // plugin's default options
        // this is private property and is  accessible only from inside the plugin
        var $element = $(element);
        var defaults = {
            //'/account/is-logged/'
            urlCheckLogin : $element.data("url-login"),
            urlNext: $element.data("url-next"),
            method  : 'get',
            dataType: 'json',
            modal   : '#modal-login',
            token   : null,
            data    : {},

            // if your plugin is event-driven, you may provide callback capabilities
            // for its events. execute these functions before or after events of your
            // plugin, so that users may customize those particular events without
            // changing the plugin's code
            verify: function( obj, event ) {

                if ( obj.settings.method == "post" && !obj.settings.token )
                    console.error( 'Token is not defined' );

                //if ( !('csrfmiddlewaretoken' in obj.settings.data))
                //    obj.settings.data['csrfmiddlewaretoken'] = null
                //
                //if ( 'csrfmiddlewaretoken' in obj.settings.data && obj.settings.token)
                //   obj.settings.data['csrfmiddlewaretoken'] = obj.settings.token;

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

            },

            check: function( obj, event, data ) {
                if ( data.is_logged == true ) {
                  obj.settings.onSuccessIsLogged( obj, event, data );
                } else {
                  obj.settings.onSuccessIsNotLogged( obj, event, data );
                }
            },

            onSuccessIsLogged: function( obj, event, data ) {
              console.log( 'onSuccessIsLogged' );
            },

            onSuccessIsNotLogged: function( obj, event, data ) {
                console.log( 'onSuccessIsNotLogged' );

                var $modal = $(obj.settings.modal);

                if (obj.settings.urlNext) {
                    $modal.find('form').attr('action', obj.settings.urlNext);
                }

                if ( $modal.is(':hidden')) {
                  $modal.modal('show');
                  event.preventDefault();
                }
            },

            onFailure: function( obj, event, status ) {
                event.preventDefault();
                console.log( 'onFailure' );
                console.log( status );
            }

        };

        // to avoid confusions, use "plugin" to reference the
        // current instance of the object
        var plugin = this;

        // this will hold the merged default, and user-provided options
        // plugin's properties will be available through this object like:
        // plugin.settings.propertyName from inside the plugin or
        // element.data('ideiaLogin').settings.propertyName from outside the plugin,
        // where "element" is the element the plugin is attached to;
        plugin.settings = {};


        // the "constructor" method that gets called when the object is created
        plugin.init = function() {

            // the plugin's final properties are the merged default and
            // user-provided options (if any)
            plugin.settings = $.extend({}, defaults, options);

            // code goes here
            // log
            var ua = navigator.userAgent,
            evnt = (ua.match(/iPad/i) || ua.match(/iPhone/)) ? 'touchstart' : 'click, focus';

            $element.on( evnt, function( event ) {
              plugin.settings.verify( plugin, event );
            });
        };

        // fire up the plugin!
        // call the "constructor" method
        plugin.init();

    };

    // add the plugin to the jQuery.fn object
    $.fn.ideiaLogin = function(options) {

        // iterate through the DOM elements we are attaching the plugin to
        return this.each(function() {

            // if plugin has not already been attached to the element
            if (undefined == $(this).data('ideiaLogin')) {

                // create a new instance of the plugin
                // pass the DOM element and the user-provided options as arguments
                var plugin = new $.ideiaLogin(this, options);

                // in the jQuery version of the element
                // store a reference to the plugin object
                // you can later access the plugin and its methods and properties like
                // element.data('ideiaLogin').publicMethod(arg1, arg2, ... argn) or
                // element.data('ideiaLogin').settings.propertyName
                $(this).data('ideiaLogin', plugin);

            }

        });

    };

    $(document).on('ready', function() {
      $('[data-trigger=login]').each(function() {
        var ua = navigator.userAgent,
        evnt = (ua.match(/iPad/i) || ua.match(/iPhone/)) ? 'touchstart' : 'click';
        var $e = $( this );
        $e.ideiaLogin( $e.data() );
        $e.on(evnt, function(e) {
          e.preventDefault();
        });
      });
    });

    $(document).ajaxComplete(function(event, jqXHR, ajaxOptions) {
      var ua = navigator.userAgent,
      evnt = (ua.match(/iPad/i) || ua.match(/iPhone/)) ? 'touchstart' : 'click';
      $('[data-trigger=login]').each(function () {
        var $e = $(this);
        $e.ideiaLogin($e.data());
        $e.on(evnt, function(e) {
          e.preventDefault();
        });
      });
    });

})(jQuery);
