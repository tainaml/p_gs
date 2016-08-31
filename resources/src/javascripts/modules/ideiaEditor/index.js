$.fn.refreshEditors = function (){

  function sendFile(files, editor) {
    var data = new FormData();
    var $editor = $(editor);
    $.each(files, function(i, value){
      data.append("file" + i, value);
    });

    var csrftoken = getCookie('csrftoken');

    $.ajax({
      data: data,
      type: "POST",
      url: "/ideia-summernote/upload",
      cache: false,
      contentType: false,
      processData: false,
      success: function(data) {
        $.each(data.urls, function(i, value){
          $editor.summernote('insertImage', value);
        });
      },
      error: function(data){
        if(data.status ==400 || data.status ==403){
          alert(data.responseJSON.message);
        }
      },
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    return false;
  }

  var $editors = this.find('[data-toggle="editor"]');

  $.each($editors, function(i, value){

    var $editor = $(value);
    var editorConfig = $editor.data('config') || {};
    var $modalLogin = $("#modal-login");
    Object.assign(editorConfig, {
      callbacks: {
        onImageUpload: function(files) {
          sendFile(files, this);
        },
        onPaste: function (e) {
            var bufferText = ((e.originalEvent || e).clipboardData || window.clipboardData).getData('Text');
            e.preventDefault();

            // Firefox fix
            setTimeout(function () {
                document.execCommand('insertText', false, bufferText);
            }, 10);
        },
        onFocus: function(e){
          var $parentForm = $editor.closest("form");
          if($parentForm.data("logged") && $parentForm.data("logged").toLowerCase() == "false"){
                $modalLogin.modal("show");
          }
        }
      }
    });

    $editor.summernote(editorConfig);
  });
};
