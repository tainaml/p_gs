$.get('/community/list-all/').done(function (data) {
  window.mentionsItems = data.communities;
  window.mentionTitles = [];
  data.communities.forEach(function (val, idx, array) {
    window.mentionTitles.push(val.title);
  });
});

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

    if (editorConfig.hasHint) {
      editorConfig.hint = {
        match: /#([\-+\w| ]+)$/,
        search: function (keyword, callback) {
          callback($.grep(mentionTitles, function (item) {
            return item.toLowerCase().indexOf(keyword.toLowerCase() || keyword) == 0;
          }));
        },
        content: function (item) {
          var content = mentionsItems.filter(function (element, index, array) {
            return element.title == item;
          })[0];

          if (content.slug && content.title) {
            return $('<a />').attr({
              href: '/'+content.slug+'/',
              title: content.title
            }).text('#'+content.title)[0];
          }
          return '';

        }
      }
    }
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
