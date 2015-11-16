;(function($) {

    var EVENT_AJAX_SUCCESS = 'asynclike.success';
    var EVENT_AJAX_ERROR   = 'asynclike.error';

    $.AsyncLike = function(element, options) {

        var defaults = {
            foo: 'bar'
        };

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

        var plugin = this;

        plugin.settings = {};

        var $element = $(element),
            element = element;

        plugin.init = function() {

            plugin.settings = $.extend({}, defaults, options);

            $element.on("click", function(e){
                e.preventDefault();

                var $self = $(this);

                $self.one(EVENT_AJAX_SUCCESS, function(event, data){
                    plugin.refresh_counters.call(this, data);
                });

                plugin.do_submit.call(this);
            });

        };

        plugin.do_submit = function(){
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
        };

        plugin.refresh_counters = function(data){
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
        };

        plugin.init();
    };

    $.fn.IdeiaAsyncLike = function(options) {
        return this.each(function() {
            if (undefined == $(this).data('IdeiaAsyncLike')) {
                var plugin = new $.AsyncLike(this, options);
                $(this).data('IdeiaAsyncLike', plugin);
            }
        });
    };

    function AsyncLikeOnReady(){
        var asyncLike = $("[data-async-like=true]");
        var asyncData = asyncLike.IdeiaAsyncLike();
    }

    $(document).ready(AsyncLikeOnReady);

})(jQuery);