webpackJsonp([3],{0:function(t,e,a){t.exports=a(102)},102:function(t,e,a){(function(e){"use strict";function n(t,a,n){var r=t.data("toggle"),i=t.parent(".dropdown-content");if("append"==r||"prepend"==r)"append"==r?n.append(a.template):n.prepend(a.template),i&&i.removeClass("open"),t[0].reset();else if("replace"==r){var o=e(a.template);n.replaceWith(o);o.find('form[data-ajaxform="true"]');n=o}t.find('[data-toggle="editor"]').summernote("reset"),n.refreshEditors();var d=e(".comment-text").find("code");return e.each(d,function(t,e){Prism.highlightElement(e)}),n}function r(){var t=location.hash;if(t){var a=e(t);if(!a.length)return;e("html,body").animate({scrollTop:a.offset().top})}}var i=document.querySelectorAll("[data-async]");i.forEach(function(e,n){var r=e.getAttribute("data-async");a.e(4,function(){(function(t){(t=a(104)(""+r))(e)}).call(this,a(103)(t))})});var o=function(t){t.preventDefault();var a=e(t.currentTarget),n=e(a.data("modal"));n.find("form").attr("action",a.data("url")),n.find("#item-id").val(a.data("item")),n.find("#item-type").val(a.data("type")),n.find("#title-item-to-remove").html(a.data("title")),n.find(".loading-container").html(""),n.find(".alert-container").html(""),n.modal("show")},d=function(t,a){var n=e(this),r=e(n.closest(".modal.fade")),i=r.find("#item-id").val(),o=r.find("#item-type").val();r.modal("hide"),r.find("form").attr("action",""),r.find("#item-id").val(""),r.find("#item-type").val(""),r.find("#title-item-to-remove").html(""),r.find(".loading-container").html(""),r.find(".alert-container").html(""),e("#"+o+"-"+i).fadeOut("slow",function(){e("#list-"+o+"-"+i).remove(),e(this).remove()})},s=function t(a,r){var i=e(this),o=e(i.data("update"));o=n(i,r,o);var d=o.find('form[data-ajaxform="true"]');e.each(d,function(a,n){var r=e(n);r.data("plugin")||(r.data("plugin","true"),r.IdeiaAjaxForm(),r.on("ajaxform.success",t))});var s=o.find("div[data-xhr]");s.renderList(),refreshAsyncLike(),e("[data-list]").on({"show.bs.dropdown":function(t){e(t.target).siblings(".comment-text").hide()},"hide.bs.dropdown":function(t){e(t.target).siblings(".comment-text").show()}});var c=e('[data-toggle="message"]');c.is(":visible")&&c.hide()};e.fn.renderList=function(){return e.each(this,function(){var t=e(this);if(!t.data("rendered")){t.data("rendered","rendered");var a,n=t.data("xhr-url");e.ajax({url:n,success:function(n){if(n.template){var r=e(n.template);t.append(r);var i=/^data-list-([0-9]+)$/;if(i.test(t.attr("id"))){var o=t.parent(".comments-children");t.children().length>0?o.removeClass("no-children"):o.addClass("no-children")}a=r.next("div[data-xhr-url]"),t.jscroll({loadingHtml:'<div class="load-async-preload"></div>',contentSelect:"#"+t.attr("id"),nextSelector:"a[data-jscroll-next]",autoTrigger:!1,callback:function(t){var a=e(".jscroll-added"),n=a.find('form[data-ajaxform="true"]');n.IdeiaAjaxForm(),n.on("ajaxform.success",s),n.refreshEditors(),a.removeClass("jscroll-added")}});var d=r.find('form[data-ajaxform="true"]');d.on("ajaxform.success",s),d.IdeiaAjaxForm(),d.refreshEditors();var c=t.find("[data-async-like]");c.IdeiaAsyncLike(),c.removeData("async-like")}},complete:function(){a&&a.length&&a.renderList();var t=e(".comment-text").find("code");e.each(t,function(t,e){Prism.highlightElement(e)})}});refreshAsyncLike(),e("[data-list]").on({"show.bs.dropdown":function(t){e(t.target).siblings(".comment-text").hide()},"hide.bs.dropdown":function(t){e(t.target).siblings(".comment-text").show()}})}})};var c=function(t){t.stopPropagation()};e(function(){var t=e(".full-post-content").find("img");e.each(t,function(t,a){var n=e(a),r=n.css("float");r&&("left"==r?n.css("margin-right",20):"right"==r&&n.css("margin-left",20))});var a=e("div[data-xhr]");a.renderList();var n=e('form[data-ajaxform="true"]');n.refreshEditors(),n.on("ajaxform.success",s),e("#confirmation-form").on("ajaxform.success",d),e(document).on("click","[data-delete-item=true]",o),e(document).on("click",".comment-dropdown",c)}),r()}).call(e,a(2))}});
//# sourceMappingURL=publication.js.map