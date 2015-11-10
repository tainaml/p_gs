require('jquery');

;(function($){

    $.fn.extend({

        loadAsync: function(){

            var loadContent = function(el){

                var $self = $(el),
                    url = $self.data("loadAsyncUrl") || $self.attr("href"),
                    timeout =  $self.data("loadAsyncTimeout") || 1e3,
                    method = $self.data("loadAsyncMethod") || "get",
                    dataType = $self.data("loadAsyncResponseType") || "json";

                setTimeout(function(){
                    $.ajax({
                        url: url,
                        method: method,
                        dataType: dataType,
                        data: {
                            'url-next': $self.data("loadAsyncUrlNext"),
                            'csrfmiddlewaretoken': $self.find("input:hidden[name='csrfmiddlewaretoken']").val()
                        },
                        success: function(data, status, xhr) {
                            $self.find(".load-async-content").html(data.template);
                        },
                        statusCode: {
                            400: function() {
                                $this.html("");
                            },
                            403: function() {
                                console.log('-- 403 Forbidden --');
                            }
                        }
                    });
                }, timeout);
            };

            return this.each(function(i,el){
                loadContent(this);
            });
        }
    });

    function LoadAsyncReady() {
        var $loadAsync = $("[data-load-async=true]");
        $loadAsync.loadAsync();
    }

    $(document).ready(LoadAsyncReady);

})(jQuery);