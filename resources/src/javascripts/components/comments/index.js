import $ from 'jquery'
import 'jscroll'
import './jquery.render-list'

var form_submit = function(event, data){
    var $form = $(this);
    var $divToUpdate = $($form.data("update"));
    $divToUpdate = setData($form, data, $divToUpdate);

    var $subforms = $divToUpdate.find("form[data-ajaxform=\"true\"]");
    $.each($subforms, function(i, value){
        var $subform = $(value);
        if(!$subform.data("plugin")){
            $subform.data("plugin", "true");
            $subform.IdeiaAjaxForm();
            $subform.on("ajaxform.success", form_submit);
        }


    });
    var $dataList = $divToUpdate.find("div[data-xhr]");
    $dataList.renderList();
    refreshAsyncLike();

};

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

    $("#" + itemType + "-" + itemId).fadeOut("slow", function(){
      $('#list-'+itemType+'-'+itemId).remove();
      $(this).remove();
    });
};

function setData($form, data, $divToUpdate){

    var action = $form.data("toggle");
    var $form_to_hide = $form.parent(".dropdown-content");

    if(action == "append" || action == "prepend") {

        if (action == "append") {
            $divToUpdate.append(data.template);
        } else {
            $divToUpdate.prepend(data.template);
        }

        if ($form_to_hide) {
            $form_to_hide.removeClass("open");
        }
        $form[0].reset();

    }else if (action=="replace"){
        var $element = $(data.template);
        $divToUpdate.replaceWith($element);
        var $newForm = $element.find("form[data-ajaxform=\"true\"]");
        $divToUpdate = $element;
    }
    $form.find('[data-toggle="editor"]').summernote('reset');
    $divToUpdate.refreshEditors();
    var $preInComment = $('.comment-text').find('code');
    $.each($preInComment, function (index, element) {
      Prism.highlightElement(element);
    });

    return $divToUpdate
}

var commentDropDown = function(event) {
  event.stopPropagation();
};

var xhr_contents = $("div[data-xhr]");
xhr_contents.renderList();
var $comment_form = $("form[data-ajaxform=\"true\"]");

$comment_form.refreshEditors();
$comment_form.on("ajaxform.success", form_submit);

$("#confirmation-form").on("ajaxform.success", functionAjaxSuccessDeleteItem);
$(document).on("click", "[data-delete-item=true]", functionOpenModalToDelete);
$(document).on('click', '.comment-dropdown', commentDropDown);
