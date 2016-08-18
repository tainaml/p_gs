require('summernote');
require('summernote/lang/summernote-pt-BR');
require('./vendor/summernote/plugins/summernote-oembed-plugin');
require('./vendor/summernote/plugins/summernote-prettyprint-plugin');

function csrfSafeMethod(method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

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
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  return false;
}

$(function init() {
  var $editor = $(document).find('[data-toggle="editor"]');
  var editorConfig = $editor.data('config') || {};
  Object.assign(editorConfig, {
    callbacks: {
      onImageUpload: function(files) {
        sendFile(files, this);
      }
    }
  });

  $editor.summernote(editorConfig);
  prettyPrint(document.querySelector('.full-post-content'));
});
