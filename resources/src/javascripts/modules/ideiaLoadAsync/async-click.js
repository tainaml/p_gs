;(function($) {

    var EVENT_AJAX_SUCCESS = 'async.click.success';
    var EVENT_AJAX_ERROR   = 'async.click.error';

    $.AsyncClick = function(element, options) {

        var defaults = {
            target: '.load-async-content'
        };

        var plugin = this;

        plugin.settings = {};

        var $element = $(element),
            element = element;

        plugin.init = function() {

            plugin.settings = $.extend({}, defaults, options);

            $element.on("click", function(e){
                e.preventDefault();
                plugin.do_submit.call(this);
            });

        };

        plugin.do_submit = function(){
            var $self = $(this);
            var url = $self.data("asyncUrl") || $self.attr("href");
            var method = $self.data("asyncMethod") || "get";
            var dataType = $self.data("asyncResponseType") || "json";

            var ajaxParams = {
                'type': method.toUpperCase(),
                'url': url,
                'cache': false,
                'data': {
                    'csrfmiddlewaretoken': $self.find("input:hidden[name='csrfmiddlewaretoken']").val() || null
                },
                success: function(data){
                    var target = $self.data("asyncTarget");
                    if(!target) {
                        $self.find(plugin.settings.target).html(data.template);
                    } else {
                        $(target).html(data.template);
                    }
                    $self.trigger(EVENT_AJAX_SUCCESS, data);
                },
                error: function(jqXHR){
                    var data = $.parseJSON(jqXHR.responseText);
                    $self.trigger(EVENT_AJAX_ERROR, [data]);
                },
                'dataType': dataType
            };

            $.ajax(ajaxParams);
        };

        plugin.init();
    };

    $.fn.IdeiaAsyncClick = function(options) {
        return this.each(function() {
            if (undefined == $(this).data('IdeiaAsyncClick')) {
                var plugin = new $.AsyncClick(this, options);
                $(this).data('IdeiaAsyncClick', plugin);
            }
        });
    };

    function AsyncClickOnReady(){
        var asyncElem = $("[data-async-module=click]");
        var asyncData = asyncElem.IdeiaAsyncClick();
    }

    $(document).ready(AsyncClickOnReady);

})(jQuery);