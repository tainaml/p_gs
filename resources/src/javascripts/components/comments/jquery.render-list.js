// import $ from 'jquery'

// $.fn.renderList = function () {

  // return $.each(this, function(){
  //       var $self = $(this);
  //       if(!$self.data("rendered")){
  //           $self.data("rendered", "rendered");
  //           var url = $self.data('xhr-url');
  //           var $childs;
  //
  //           var request = $.ajax({
  //               url: url,
  //               success: function(data){
  //
  //                   if(data.template){
  //                       var $element = $(data.template);
  //
  //                       $self.append($element);
  //                       var regex = /^data-list-([0-9]+)$/;
  //                       if (regex.test($self.attr('id'))) {
  //                           var $parentSelf = $self.parent('.comments-children');
  //                           if ($self.children().length > 0) {
  //                               $parentSelf.removeClass('no-children');
  //                           } else {
  //                               $parentSelf.addClass('no-children');
  //                           }
  //                       }
  //
  //                       $childs = $element.next('div[data-xhr-url]');
  //                       $self.jscroll({
  //                           loadingHtml: '<div class="load-async-preload"></div>',
  //                           contentSelect: "#" + $self.attr("id"),
  //                           nextSelector: "a[data-jscroll-next]",
  //                           autoTrigger: false,
  //                           callback: function(data){
  //                               var $div_jscroll = $(".jscroll-added");
  //                               var $jscroll_subforms = $div_jscroll.find("form[data-ajaxform=\"true\"]");
  //                               $jscroll_subforms.IdeiaAjaxForm();
  //                               $jscroll_subforms.on("ajaxform.success", form_submit);
  //                               $jscroll_subforms.refreshEditors();
  //                               $div_jscroll.removeClass("jscroll-added");
  //                           }
  //                       });
  //
  //                       var $subforms = $element.find("form[data-ajaxform=\"true\"]");
  //                       $subforms.on("ajaxform.success", form_submit);
  //                       $subforms.IdeiaAjaxForm();
  //                       $subforms.refreshEditors();
  //
  //                       var async_like = $self.find('[data-async-like]');
  //                       async_like.IdeiaAsyncLike();
  //                       async_like.removeData("async-like");
  //                   }
  //
  //               },
  //               complete: function(){
  //                   if($childs && $childs.length){
  //                       $childs.renderList();
  //                   }
  //
  //                   var $preInComment = $('.comment-text').find('code');
  //                   $.each($preInComment, function (index, element) {
  //                     Prism.highlightElement(element);
  //                   });
  //               }
  //           });
  //
  //           refreshAsyncLike();
  //       }
  //
  //   });
  var pluginName = "renderList",
			defaults = {
				propertyName: "value"
			};

		// The actual plugin constructor
		function Plugin ( element, options ) {
			this.element = element;
			this.settings = $.extend( {}, defaults, options );
			this._defaults = defaults;
			this._name = pluginName;
			this.init();
		}

    // Avoid Plugin.prototype conflicts
		$.extend( Plugin.prototype, {
			init: function() {

				// Place initialization logic here
				// You already have access to the DOM element and
				// the options via the instance, e.g. this.element
				// and this.settings
				// you can add more functions like the one below and
				// call them like the example below
        console.log( $(this.element).data('xhrUrl') );
        this.attachList( $(this.element).data('xhrUrl') );
			},
      attachList: function (url) {
        $.get(url)
        .done(function (data) {
          if( data.template ) {
            console.log( data.template );
          }
        })
        .fail( function (data) {

        })
        .always( function (data) {

        });
      }
		} );

    $.fn[ pluginName ] = function( options ) {
			return this.each( function() {
				if ( !$.data( this, "plugin_" + pluginName ) ) {
					$.data( this, "plugin_" +
						pluginName, new Plugin( this, options ) );
				}
			} );
		};
// };
