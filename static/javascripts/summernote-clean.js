function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
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
                error: function(data){
                    if(data.status ==400 || data.status ==403){
                        alert(data.responseJSON.message);
                    }
                }
                ,
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
    return false;
}


$(function(){
    var $editors = $("[data-toggle='editor']");

    $.each($editors, function(i, value){
       var $element = $(value);
       var editorConfig = $element.data('config') || {};

       Object.assign(editorConfig, {
          callbacks: {

          onPaste: function (e) {
                console.log("HEheh");
                var bufferText = ((e.originalEvent || e).clipboardData || window.clipboardData).getData('Text');
                e.preventDefault();

                // Firefox fix
                setTimeout(function () {
                    document.execCommand('insertText', false, bufferText);
                }, 10);
            },
          onImageUpload: function(files) {
                sendFile(files, this);
              }
          }
        });
        $element.summernote(editorConfig);
    });
});


