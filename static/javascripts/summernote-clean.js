$(function(){
    var $editors = $("[data-toggle='editor']");
    $.each($editors, function(i, value){
       var $element = $(value);
       var editorConfig = $element.data('config') || {};
        console.log(editorConfig);
       Object.assign(editorConfig, {
          callbacks: {

          onPaste: function (e) {

                var bufferText = ((e.originalEvent || e).clipboardData || window.clipboardData).getData('Text');
                e.preventDefault();

                // Firefox fix
                setTimeout(function () {
                    document.execCommand('insertText', false, bufferText);
                }, 10);
            }
          }
        });
        $element.summernote(editorConfig);
    });
});


