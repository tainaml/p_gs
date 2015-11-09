//
// $('#element').donetyping(callback[, timeout=1000])
// Fires callback when a user has finished typing. This is determined by the time elapsed
// since the last keystroke and timeout parameter or the blur event--whichever comes first.
//   @callback: function to be called when even triggers
//   @timeout:  (default=1000) timeout, in ms, to to wait before triggering event if not
//              caused by blur.
// Requires jQuery 1.7+
//
;(function($){

    $.fn.extend({

        autocomplete: function(){

            var EVENT_AJAX_SUCCESS = 'autocomplete.success';
            var EVENT_AJAX_ERROR   = 'autocomplete.error';

            var $self = $(this),
                $target = $($self.data("autocompleteTarget")),
                timeout = $self.data("autocompleteTimeout") || 1e3, // 1 second default timeout
                method = $self.data("autocompleteMethod") || "get",
                dataType = $self.data("autocompleteDataType") || "json",
                url = $self.data("autocompleteUrl") || $self.attr("href");

            var timeoutReference,
                doneTyping = function(el){
                    if (!timeoutReference) return;
                    timeoutReference = null;

                    var ajaxParams = {
                        'type': method.toUpperCase(),
                        'url': url,
                        'cache': false,
                        success: function(data){
                            $target.html(data.template);
                            $target.show();
                            $self.trigger(EVENT_AJAX_SUCCESS, data);
                        },
                        error: function(jqXHR){
                            var data = $.parseJSON(jqXHR.responseText);
                            $self.trigger(EVENT_AJAX_ERROR, [data]);
                        },
                        'dataType': dataType,
                        'data': $self.closest('form').serialize()
                    };
                    $.ajax(ajaxParams);

                    //callback.call(el);
                },
                hideTyping = function(el){
                    if($target.length && $target.is(':visible')){
                        $target.hide().empty();
                    }
                };

            return this.each(function(i,el){

                var $el = $(el);

                // Chrome Fix (Use keyup over keypress to detect backspace)
                // thank you @palerdot
                $el.is(':input') && $el.on('keyup keypress',function(e){

                    // This catches the backspace button in chrome, but also prevents
                    // the event from triggering too premptively. Without this line,
                    // using tab/shift+tab will make the focused element fire the callback.
                    if (e.type=='keyup' && e.keyCode!=8) return;

                    // Check if timeout has been set. If it has, "reset" the clock and
                    // start over again.
                    if (timeoutReference) clearTimeout(timeoutReference);
                    timeoutReference = setTimeout(function(){

                        // if we made it here, our timeout has elapsed. Fire the
                        // callback
                        doneTyping(el);

                    }, timeout);

                }).on('blur',function(e){

                    // If we can, fire the event since we're leaving the field
                    doneTyping(el);
                    //hideTyping(el);

                });
            });

        }

    });

    function AutocompleteReady() {
        $("[data-autocomplete=true]").autocomplete();
    }

    $(document).ready(AutocompleteReady);

})(jQuery);

