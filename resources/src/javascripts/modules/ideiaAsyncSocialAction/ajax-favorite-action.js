require('./when-event.js');

;(function ( $, window, document ) {
    var pluginName = 'ajaxFavoriteAction',
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
            $that.parent().toggleClass( result.acted ? 'item-active' : '' );
        });

        this.activeFavourite();
    };
    Plugin.prototype.activeFavourite = function () {
        var $that = this;

        $( $that.element ).on( 'click.active', function ( event ) {
            var ajaxUrl = event.currentTarget.href;
            event.preventDefault();

            $.getJSON( ajaxUrl, function ( result ) {
                $($that.element).parent().toggleClass(result.acted ? $that._defaults.activeClass : '' );
            });
        });
    }

    $.fn[pluginName] = function ( options ) {
        return this.each(function () {
            if ( !$.data ( this, "plugin_" + pluginName )) {
                $.data ( this, "plugin_" + pluginName,
                new Plugin( this, options ));
            }
        });
    };

    $('[data-action=favourite]').ajaxFavoriteAction();

})(jQuery, window, document);