require('./vendor/code-prettify/prettify');
require('summernote');
require('summernote/lang/summernote-pt-BR');
require('./vendor/summernote/plugins/summernote-oembed-plugin');
require('./vendor/summernote/plugins/summernote-prettyprint-plugin');

prettyPrint(document.querySelector('.full-post-content'));
