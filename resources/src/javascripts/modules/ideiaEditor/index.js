$.fn.refreshEditors = function (){

  function sendFile(files, editor) {
    var data = new FormData();
    var $editor = $(editor);
    $.each(files, function(i, value){
      data.append('file' + i, value);
    });

    var csrftoken = getCookie('csrftoken');

    $.ajax({
      data: data,
      type: 'POST',
      url: '/ideia-summernote/upload',
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
          xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
      }
    });

    return false;
  }

  const $editors = this.find('[data-toggle="editor"]');

  $.each($editors, function(i, value) {

    var $editor = $(value);
    let editorConfig = $editor.data('config') || {};
    let hintURI = $editor.data('hintUrl');

    if (editorConfig.hasHint) {
      editorConfig.hint = [{
        match: /#([\-+\w| ]+)$/,
        search: (keyword, callback) => {
          $.getJSON('/community/list-all/', { criteria: keyword },
            data => {
              callback(data.communities);
            }
          );
        },
        template: item => `<img src="${item.thumb_url}" width="16" height="16" alt="${item.title}" /> ${item.title}`,
        content: item => {
          if (item.slug && item.title) {
            let tempself = $(this);

            setTimeout(function () {
              tempself.trigger('summernote.change');
            }, 11);

            return $('<a />').attr({
              href: `/${item.slug}/`,
              title: item.title
            }).text(`#${item.title}`)[0];
            $editor.val($editor.summernote('code'));
          }
          return '';
        },
      }];
    }

    if (editorConfig.hasHint && hintURI) {
      editorConfig.hint.push({
        match: /\B@(\w*)$/,
        search: (keyword, callback) => {
          if (keyword) {
            $.getJSON(hintURI, { term: keyword },
              data => {
                callback(data.users);
              }
            );
          }
        },
        template: item => `<img src="${item.thumb_url}" width="16" height="16" alt="${item.full_name}" /> ${item.full_name}`,

        content: item => {
          if (item.username && item.full_name) {
            // TODO:
            // A url ainda está fixa, fazer a tradução
            let tempself = $(this);
            setTimeout(function () {
              tempself.trigger('summernote.change');
            }, 11);
            return $('<a />').attr({
              href: `/perfil/${item.username}/`,
              title: item.full_name
            }).text(`@${item.full_name}`)[0];
          }
          return '';
        },
      });
    }

    var $modalLogin = $('#modal-login');
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
        onFocus: function(e) {
          var $parentForm = $editor.closest('form');
          if($parentForm.data('logged') && $parentForm.data('logged').toLowerCase() == 'false') {
            $modalLogin.modal('show');
          }
        },
      }
    });

    $editor.summernote(editorConfig);
  });
};
