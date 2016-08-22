$.fn.refreshEditors = function () {
  var $editors = this.find('[data-toggle="editor"]');

  return $.each($editors, function(i, value){
    var $editor = $(value);
    var editorConfig = $editor.data('config') || {};

    Object.assign(editorConfig, {
      callbacks: {
        onImageUpload: function(files) {
          sendFile(files, this);
        }
      }
    });

    $editor.summernote(editorConfig);
  });
};
