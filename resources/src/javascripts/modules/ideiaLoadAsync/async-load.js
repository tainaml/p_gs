;(function($) {

    var EVENT_AJAX_SUCCESS = 'async.load.success';
    var EVENT_AJAX_ERROR   = 'async.load.error';

    $.AsyncLoad = function(element, options) {

        var plugin = this;

        plugin.settings = {};

        var $element = $(element),
            element = element;

        plugin.init = function() {
            plugin.do_submit(element);

        };

        plugin.do_submit = function(el){
            var $self = $(el),
                url = $self.data("loadAsyncUrl") || $self.attr("href"),
                method = $self.data("loadAsyncMethod") || "get",
                dataType = $self.data("loadAsyncResponseType") || "json",
                timeout =  $self.data("loadAsyncTimeout") || 1e3;

            var ajaxParams = {
                url: url,
                method: method,
                dataType: dataType,
                data: {
                    'url-next': $self.data("loadAsyncUrlNext"),
                    'csrfmiddlewaretoken': $self.find("input:hidden[name='csrfmiddlewaretoken']").val()
                },
                success: function(data, status, xhr) {
                    var target = $self.data("loadAsyncTarget");
                    if(!target) {
                        $self.find(".load-async-content").html(data.template);
                    } else {
                        $(target).html(data.template);
                    }
                    $self.trigger(EVENT_AJAX_SUCCESS, data);
                },
                statusCode: {
                    400: function() {
                        $this.html("");
                    },
                    403: function() {
                        console.log('-- 403 Forbidden --');
                    }
                }
            };

            setTimeout(function(){
                $.ajax(ajaxParams);
            }, timeout);
        };

        plugin.init();
    };

    $.fn.loadAsync = function(options) {
        return this.each(function() {
            if (undefined == $(this).data('IdeiaAsyncLoad')) {
                var plugin = new $.AsyncLoad(this, options);
                $(this).data('IdeiaAsyncLoad', plugin);
            }
        });
    };

    function AsyncLoadOnReady(){
        var asyncElem = $("[data-load-async=true]");
        var asyncData = asyncElem.loadAsync();
    }

    $(document).ready(AsyncLoadOnReady);

})(jQuery);