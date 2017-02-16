'use strict';

import carousel from './components/publication-carousel';


var functionOpenModalToDelete = function(e) {
  e.preventDefault();

  var $btn = $(e.currentTarget),
    $modal = $($btn.data("modal"));

  $modal.find("form").attr("action", $btn.data("url"));
  $modal.find("#item-id").val($btn.data("item"));
  $modal.find("#item-type").val($btn.data("type"));
  $modal.find("#title-item-to-remove").html($btn.data("title"));
  $modal.find(".loading-container").html("");
  $modal.find(".alert-container").html("");
  $modal.modal("show");
};

var functionAjaxSuccessDeleteItem = function(e, data) {
  var $this = $(this),
    $modal = $($this.closest(".modal.fade")),
    itemId = $modal.find("#item-id").val(),
    itemType = $modal.find("#item-type").val();

  $modal.modal("hide");
  $modal.find("form").attr("action", "");
  $modal.find("#item-id").val("");
  $modal.find("#item-type").val("");
  $modal.find("#title-item-to-remove").html("");
  $modal.find(".loading-container").html("");
  $modal.find(".alert-container").html("");

  $("#" + itemType + "-" + itemId).fadeOut("slow", function() {
    $('#list-' + itemType + '-' + itemId).remove();
    $(this).remove();
  });
};

function setData($form, data, $divToUpdate) {

  var action = $form.data("toggle");
  var $form_to_hide = $form.parent(".dropdown-content");

  if (action == "append" || action == "prepend") {

    if (action == "append") {
      $divToUpdate.append(data.template);
    } else {
      $divToUpdate.prepend(data.template);
    }

    if ($form_to_hide) {
      $form_to_hide.removeClass("open");
    }
    $form[0].reset();

  } else if (action == "replace") {
    var $element = $(data.template);
    $divToUpdate.replaceWith($element);
    var $newForm = $element.find("form[data-ajaxform=\"true\"]");
    $divToUpdate = $element;
  }
  $form.find('[data-toggle="editor"]').summernote('reset');
  $divToUpdate.refreshEditors();
  var $preInComment = $('.comment-text').find('code');
  $.each($preInComment, function(index, element) {
    Prism.highlightElement(element);
  });

  return $divToUpdate
}

var form_submit = function(event, data) {
  var $form = $(this);
  var $divToUpdate = $($form.data("update"));
  $divToUpdate = setData($form, data, $divToUpdate);

  var $subforms = $divToUpdate.find("form[data-ajaxform=\"true\"]");
  $.each($subforms, function(i, value) {
    var $subform = $(value);
    if (!$subform.data("plugin")) {
      $subform.data("plugin", "true");
      $subform.IdeiaAjaxForm();
      $subform.on("ajaxform.success", form_submit);
    }
  });

  var $dataList = $divToUpdate.find("div[data-xhr]");
  $dataList.renderList();
  refreshAsyncLike();
  $('[data-list]').on({
    'show.bs.dropdown': function(event) {
      $(event.target).siblings('.comment-text').hide()
    },
    'hide.bs.dropdown': function(event) {
      $(event.target).siblings('.comment-text').show()
    }
  });

  var $msgEmpty = $('[data-toggle="message"]');
  if ($msgEmpty.is(':visible')) {
    $msgEmpty.hide();
  }
};

$.fn.renderList = function() {

  return $.each(this, function() {


    var $self = $(this);

    if (!$self.data("rendered")) {
      $self.data("rendered", "rendered");
      var url = $self.data('xhr-url');
      var $childs;

      var request = $.ajax({
        url: url,
        success: function(data) {

          if (data.template) {
            var $element = $(data.template);

            $self.append($element);
            var regex = /^data-list-([0-9]+)$/;
            if (regex.test($self.attr('id'))) {
              var $parentSelf = $self.parent('.comments-children');
              if ($self.children().length > 0) {
                $parentSelf.removeClass('no-children');
              } else {
                $parentSelf.addClass('no-children');
              }
            }

            $childs = $element.next('div[data-xhr-url]');
            $self.jscroll({
              loadingHtml: '<div class="load-async-preload"></div>',
              contentSelect: "#" + $self.attr("id"),
              nextSelector: "a[data-jscroll-next]",
              autoTrigger: false,
              callback: function(data) {
                var $div_jscroll = $(".jscroll-added");
                var $jscroll_subforms = $div_jscroll.find("form[data-ajaxform=\"true\"]");
                $jscroll_subforms.IdeiaAjaxForm();
                $jscroll_subforms.on("ajaxform.success", form_submit);
                $jscroll_subforms.refreshEditors();
                $div_jscroll.removeClass("jscroll-added");
              }
            });

            var $subforms = $element.find("form[data-ajaxform=\"true\"]");
            $subforms.on("ajaxform.success", form_submit);
            $subforms.IdeiaAjaxForm();
            $subforms.refreshEditors();

            var async_like = $self.find('[data-async-like]');
            async_like.IdeiaAsyncLike();
            async_like.removeData("async-like");
          }

        },
        complete: function() {
          if ($childs && $childs.length) {
            $childs.renderList();
          }

          var $preInComment = $('.comment-text').find('code');
          $.each($preInComment, function(index, element) {
            Prism.highlightElement(element);
          });
        }
      });

      refreshAsyncLike();
      $('[data-list]').on({
        'show.bs.dropdown': function(event) {
          $(event.target).siblings('.comment-text').hide()
        },
        'hide.bs.dropdown': function(event) {
          $(event.target).siblings('.comment-text').show()
        }
      });
    }

  });
};

var commentDropDown = function(event) {
  event.stopPropagation();
};

carousel($('[data-toggle="carousel"]'))

$(function() {
  var imagesContent = $('[data-target="post-content"]').find('img');
  $.each(imagesContent, function(index, image) {
    var $image = $(image);
    var imageFloat = $image.css('float');
    if (imageFloat) {
      $image.css(`margin-${imageFloat}`, 20);
    }
  });

  var xhr_contents = $("div[data-xhr]");
  xhr_contents.renderList();
  var $comment_form = $("form[data-ajaxform=\"true\"]");

  $comment_form.refreshEditors();
  $comment_form.on("ajaxform.success", form_submit);

  $("#confirmation-form").on("ajaxform.success", functionAjaxSuccessDeleteItem);
  $(document).on("click", "[data-delete-item=true]", functionOpenModalToDelete);
  $(document).on('click', '.comment-dropdown', commentDropDown);
});

function moveToHashPosition() {
  var _hash = location.hash;
  if (_hash) {

    var $target = $(_hash);

    if (!$target.length) {
      return;
    }

    $('html,body').animate({
      'scrollTop': $target.offset().top
    })
  }
}

moveToHashPosition();