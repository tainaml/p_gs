$(function init () {
  let $selector = $('[data-toggle="editor"]');
  let config = $selector.data('config') || {};
  // let config = {};
  $selector.summernote(config);
});
