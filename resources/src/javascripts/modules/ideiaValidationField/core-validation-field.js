(function($) {

    $._IdeiaValidation = function(element, options) {
        var timeoutReference = null;

        var STATUS_CHECKING = 'checking',
            STATUS_CHECKED = 'checked',
            STATUS_AVAILABLE = 'has-success',
            STATUS_ERROR = 'has-error';

        var defaults = {
            urlCheckValidation : null,
            timeout: 1000,
            messageErrorRegex: 'Insira um "slug" válido consistindo de letras, números, sublinhados (_) ou hífens.',
            regex: '^([a-z0-9]+((-|_)[a-z0-9]+?)*)$',
            async: false,
            searchBy: 'username',
            data : {}
        };

        var plugin = this;
        plugin.settings = {};

        var $element = $(element),
            $formGroup = $element.closest('.form-group');

        plugin.init = function() {
            plugin.settings = $.extend({}, defaults, options);
            console.log(plugin);

            $(document).on( 'input', '#' + $element.attr('id'), function( e ) {
                plugin.clearEvents();
                plugin.verify( e );
            });
        };

        plugin.verify = function( e ) {
            var $e = $(e.target);

            var regex = new RegExp(plugin.settings.regex);

            console.log(regex);

            if ( regex.test($e.val()) == false ) {
                plugin.addError(plugin.settings.messageErrorRegex);
                return;
            }

            if ( plugin.settings.async ) {

                if ( timeoutReference ) clearTimeout( timeoutReference );

                timeoutReference = setTimeout(function() {
                    plugin.settings.data[plugin.settings.searchBy] = $e.val().trim();
                    $.ajax({
                        url: plugin.settings.urlCheckValidation,
                        method: 'get',
                        dataType: 'json',
                        data: plugin.settings.data,
                        beforeSend: function() {
                            plugin.clearEvents();
                        },
                        success: function(data) {
                            plugin.check( data );
                        },
                        error: function(xhr) {
                            plugin.onFailure( xhr );
                        }
                    });

                }, plugin.settings.timeout);
            }
        };

        plugin.check = function( data ) {
            $element.data('ideiaValidationStatus', STATUS_CHECKED);
            plugin.addSuccess(data.message);
        };

        plugin.onFailure = function( xhr ) {
            console.log('onFailure - Validation');
            $element.data('ideiaValidationStatus', STATUS_CHECKED);
            var data = $.parseJSON(xhr.responseText);
            plugin.addError(data.message);
        };

        plugin.clearEvents = function() {
            $formGroup.removeClass(STATUS_AVAILABLE).removeClass(STATUS_ERROR).addClass(STATUS_CHECKING);
            $formGroup.find('.errorlist').remove();
            $formGroup.find('.check-username-response').remove();
        };

        plugin.addError = function( msg ) {
            plugin.addHelpBlock(STATUS_CHECKING, STATUS_ERROR, msg);
        };

        plugin.addSuccess = function( msg ){
            plugin.addHelpBlock(STATUS_CHECKING, STATUS_AVAILABLE, msg);
        };

        plugin.addHelpBlock = function(removeStatus, addStatus, msg) {
            var $messageResponse = $('<span/>');
            $messageResponse.addClass('help-block check-username-response').text( msg );
            $formGroup.removeClass(removeStatus).addClass(addStatus).append($messageResponse);
        };

        plugin.init();

    };

    $.fn.IdeiaValidation = function(options) {
        return this.each(function() {
            if (undefined == $(this).data('IdeiaValidation')) {
                var plugin = new $._IdeiaValidation(this, options);
                $(this).data('IdeiaValidation', plugin);
            }
        });
    };

    $( document ).on( 'ready', function() {
        $( '[data-toggle=validation]' ).each( function () {
            var $e = $( this );
            $e.IdeiaValidation( $e.data() );
        });
    });

})(jQuery);