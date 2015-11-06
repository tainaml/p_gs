(function($){
    'use strict';

    $.fn.IdeiaAutocomplete = function(){

        var isLocked = false;
        var EVENT_AJAX_SUCCESS = 'autocomplete.success';
        var EVENT_AJAX_ERROR   = 'autocomplete.error';

        function doCancel(e){
            e.preventDefault();
            var $self = $(this);

            $self.one(EVENT_AJAX_SUCCESS, function(event, data){});

            if($self.val().length > 2){
                console.log($self.val());
            }
            //doSubmit.call(this);
        }

        function doSubmit(e){
            var $self = $(this);
            var url = $self.attr('href') || $self.data('url');
            var method = $self.data('method') || 'get';

            var ajaxParams = {
                'type': method.toUpperCase(),
                'url': url,
                'cache': false,
                success: function(data){
                    $self.trigger(EVENT_AJAX_SUCCESS, data);
                },
                error: function(jqXHR){
                    var data = $.parseJSON(jqXHR.responseText);
                    $self.trigger(EVENT_AJAX_ERROR, [data]);
                },
                'dataType': 'json',
                'data': $self.serialize()
            };
            $.ajax(ajaxParams);
        }

        function setup(){
            var $self = $(this);
            $self.on('keyup', doCancel);
        }

        return this.each(function(i, el){
            setup.call(this);
        });
    };

    function IdeiaAutocompleteReady(){
        //var autocomplete = $("[data-autocomplete=true]");
        //autocomplete.IdeiaAutocomplete();
    }

    $(document).ready(IdeiaAutocompleteReady);

})(jQuery);