(function($){
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

})(jQuery);