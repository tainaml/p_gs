$(function init () {
  let $selector = $('[data-toggle="editor"]');
  let config = $selector.data('config') || {};
  // let config = {};
  try{
    $selector.summernote(config);
  }catch(err){}

});
