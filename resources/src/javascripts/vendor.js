// require('./vendor/code-prettify/prettify');
require('summernote');
require('./vendor/prismjs');
require('summernote/lang/summernote-pt-BR');
require('./vendor/summernote/plugins/summernote-oembed-plugin');
require('./vendor/summernote/plugins/summernote-prettyprint-plugin');
require('./modules/ideiaEditor');

var $preInPost = $('.full-post-content').find('code');

$.each($preInPost, function (index, element) {
  Prism.highlightElement(element);
});

$('[data-target="container-editor"]').refreshEditors();
