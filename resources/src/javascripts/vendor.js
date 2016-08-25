require('./vendor/code-prettify/prettify');
require('summernote');
require('summernote/lang/summernote-pt-BR');
require('./vendor/summernote/plugins/summernote-oembed-plugin');
require('./vendor/summernote/plugins/summernote-prettyprint-plugin');
require('./modules/ideiaEditor');

PR.prettyPrint();
$('[data-target="container-editor"]').refreshEditors();
