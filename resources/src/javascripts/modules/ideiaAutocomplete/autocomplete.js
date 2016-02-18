;(function($){

    $.fn.extend({

        autocomplete: function(){

            var EVENT_AJAX_SUCCESS = 'autocomplete.success';
            var EVENT_AJAX_ERROR   = 'autocomplete.error';

            var $self = $(this),
                target = $self.data("autocompleteTarget"),
                $target = $(target),
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
                            $self.attr('data-autocomplete-response', true);
                            $self.trigger(EVENT_AJAX_SUCCESS, data);
                            $('[data-toggle="custom-scroll"] > .float-notifcations').perfectScrollbar();
                        },
                        error: function(jqXHR){
                            var data = $.parseJSON(jqXHR.responseText);
                            $self.trigger(EVENT_AJAX_ERROR, [data]);
                        },
                        'dataType': dataType,
                        'data': $self.closest('form').serialize()
                    };
                    $.ajax(ajaxParams);
                },
                hideTyping = function(e){
                    if(!$(e.target).is("[data-autocomplete=true]") && !$(e.target).closest(target).length){
                        if($target.is(":visible")) {
                            $target.hide();
                        }
                    }
                },
                showTyping = function(e){
                    if($self.data('autocompleteResponse') == true && $target.length && $target.is(':hidden')){
                        $('[data-toggle="custom-scroll"] > .float-notifcations').perfectScrollbar();
                        $target.show();
                    }
                };

            $(document).on("click", function(e){
                hideTyping(e);
            });

            return this.each(function(i,el){
                var $el = $(el);
                $el.is(':input') && $el.on('input',function(e){
                    if (e.type=='keyup' && e.keyCode!=8) return;
                    if (timeoutReference) clearTimeout(timeoutReference);
                    timeoutReference = setTimeout(function(){
                        doneTyping(el);
                    }, timeout);
                }).on('focus', function(e){
                    showTyping(e);
                });
                $(document).on('keydown', function (e) {
                    var eventKey = e.keyCode;
                    if ($el.is(':focus') && $('#dropdown-search').is(':visible')) {
                        switch (eventKey) {
                            case 13:
                                triggerItem(e);
                                return false;
                                break;
                            case 38:
                                activeSearchItem('up');
                                break;
                            case 40:
                                activeSearchItem('down');
                                break;
                        }
                    }
                });
            });
        }
    });

    // Número negativo porque o index de elementos do DOM começa em 0 (zero).
    var itemActive = -1;
    function activeSearchItem (direction, incrementer) {
        var searchItems = $('#dropdown-search').find('li');
        var itemsLength = searchItems.length - 1;
        var firstPosition = 0;
        searchItems.removeClass('active');

        direction == 'down' ? itemActive++ : itemActive--;

        if (itemActive >= firstPosition && itemActive <= itemsLength) {
            searchItems.eq(itemActive).addClass('active');
        } else if (itemActive <= firstPosition) {
            searchItems.eq(firstPosition).addClass('active');
            itemActive = firstPosition;
        } else if (itemActive > itemsLength) {
            searchItems.last().addClass('active');
            itemActive = itemsLength;
        }
    }

    function triggerItem (e) {
        e.stopPropagation();
        var item = $('#dropdown-search').find('.active a');
        location.href = item.attr('href');
    }

    function AutocompleteReady() {
        $("[data-autocomplete=true]").autocomplete();
    }

    $(document).ready(AutocompleteReady);

})(jQuery);