if ( $( '[data-page="courses"]' ).length ) {
  console.log( 'Troll' );
  $( '[data-form-send]' ).on( 'change', function onChangeSelectSendVideoForm () {
    var $self = $(this);
    var $form = $self.closest( 'form[data-form-send-enables]' );
    if ( $form.length ) {
        $form.trigger('submit');
    }
  });
}
