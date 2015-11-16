require('./when-event.js');

(function($){

    'use strict';

    $.fn.IdeiaAsyncLike = function(action) {

        var defaultOptions = {
            'parentGroup'   : '.async-like-group',
            'cssClass': {
                'like'      : 'liked',
                'unlike'    : 'unliked'
            },
            'elem': {
                'like'      : '[data-social-action="like"]',
                'unlike'    : '[data-social-action="unlike"]'
            },
            'inverseAction': {
                'like'      : 'unlike',
                'unlike'    : 'like'
            }
        };

        var EVENT_AJAX_SUCCESS = 'asynclike.success';
        var EVENT_AJAX_ERROR   = 'asynclike.error';

        function ascynLikeCancel (e) {
            e.preventDefault();

            var $self = $(this);

            $self.one(EVENT_AJAX_SUCCESS, function(event, data){
                doRefreshCounters.call(this, data);
            });

            doSubmit.call(this);
        }

        function doRefreshCounters (data) {
            var $self = $(this),
                $selfParent = $self.closest($self.data('parentGroup') || defaultOptions.parentGroup),
                $socialAction = $self.data('socialAction');

            var c = defaultOptions.cssClass,
                e = defaultOptions.elem,
                i = defaultOptions.inverseAction;

            $selfParent.find(e[$socialAction]).removeClass(c[$socialAction]);
            $selfParent.find(e[i[$socialAction]]).removeClass(c[i[$socialAction]]);

            if(data.action_response){
                $selfParent.find(e[$socialAction]).addClass(c[$socialAction]);
            }

            var tempElemLike = $($self.data('target-like'));
            var tempElemUnLike = $($self.data('target-unlike'));

            $.each(tempElemLike, function(){
                var $el = $(this);
                $el.html(data.likes);
            });

            $.each(tempElemUnLike, function(){
                var $el = $(this);
                $el.html(data.unlikes);
            });
        }

        function doSubmit () {
            var $self = $(this);
            var url = $self.attr('href') || $self.data('url');
            var method = $self.data('method') || 'get';

            var ajaxParams = {
                type: method.toUpperCase(),
                url: url,
                cache: false,
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
            $self.on('click', ascynLikeCancel);
        }

        $(this).each(function(){
            setup.call(this);
        });

    };

    function ideiaAsyncLikeOnReady(){
        var asyncLike = $('[data-async-like]');
        asyncLike.IdeiaAsyncLike();
    }

    $(document).ready(ideiaAsyncLikeOnReady);

})(jQuery);