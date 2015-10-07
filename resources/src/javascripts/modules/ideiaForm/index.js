;(function($){
    'use strict';

    $.fn.whenEvent = function(events){

        var elementIndex, $element, deferred, eventIndex;

        if(!$.isArray(events)){
            events = [events];
        }

        var deferreds = [];

        for(elementIndex=0;elementIndex < this.length; elementIndex++){
            $element = $(this[elementIndex]);
            for(eventIndex=0; eventIndex < events.length; eventIndex++){
                deferred = $.Deferred();
                deferreds.push(deferred);
                $element.one(events[eventIndex], deferred.resolve)
            }
        }
        return $.when.apply(null, deferreds);
    };

    $.fn.IdeiaAjaxForm = function(action){

        var EVENT_AJAX_VALIDATION = 'ajaxform.validation';

        function formCancelSubmit(e){
            e.preventDefault();
            var $self = $(this);
            $self.whenEvent(EVENT_AJAX_VALIDATION).done(doSubmit);
            $self.one(EVENT_AJAX_VALIDATION, doValidation);

            $(document).on(EVENT_AJAX_VALIDATION, $self, function(event, addError){

            });

            $self.trigger(EVENT_AJAX_VALIDATION, function _addError(field, error, unique=false){
                console.log("ADDERROR");
                var event = this;
                var $target = $(event.currentTarget);

                var errors = $(this).data('form-erros');
            });
        }

        function doValidation(event, addError){

            addError.call(event, 'text', 'Meu erro');
        }

        function doSubmit(){
        }

        function setup(){
            var $self = $(this);
            $self.data('ajax-form-enabled', true);
            $self.data('form-errors', []);
            $self.on('submit', formCancelSubmit);
        }

        $(this).each(function(){
            setup.call(this);
        });

    };

    function ideiaFormOnReady(){
        var ajaxForms = $('form[data-ajaxform]');
        ajaxForms.IdeiaAjaxForm();
    }

    $(document).ready(ideiaFormOnReady);

})(jQuery);