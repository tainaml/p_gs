module.exports = ( name ) => {
  const $commitBox = $( name );
  const $commitText = $commitBox.find( '[data-toggle="commit-text"]');
  let $countdownLength = $commitBox.find( '[data-target="countdown-length"]');


  $commitText.on( 'input', function ( event ) {
    const $this = $( event.currentTarget );
    let boxLength = $this.val().length;

    if ( boxLength > $countdownLength.data( 'maxLength' )) {
      $this.val($(this).val().substring(0, $countdownLength.data( 'maxLength' )));
      boxLength = $this.val().length;
    }

    $countdownLength.text( $countdownLength.data( 'maxLength' ) - boxLength );
  });
}