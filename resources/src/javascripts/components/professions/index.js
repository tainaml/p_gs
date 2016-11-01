$(document).on('input', '[data-filter="textbox"]', function ( event ) {
    var $this = $( event.currentTarget );
    var timeout;

    if ( event.type=='keyup' && event.keyCode!=8 ) return;

    if ( !timeout ) {
      timeout = setTimeout( function () {
        $this.closest('form').submit();
      }, 500 );
    } else {
      clearTimeout( timeout );
    }

    console.log( $this );
});

$(document).on('change',  '[data-filter="select"]', function( event ) {
    var $this = $( event.currentTarget );
        $this.closest('form').submit();
});

$('[data-toggle="filter"]').on("ajaxform.success", function ( event, data ) {

});
