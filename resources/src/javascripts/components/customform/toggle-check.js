module.exports = ( check, dataTarget ) => {
  const $check = $( check )
  const $target = $( `[${dataTarget}]` )

  if ($check.is(':checked')) {
    console.log($check.val())
  }

  $check.on({
    change: function ( event ) {
      const $this = $( event.currentTarget )
      $target.hide()
      $target.find(':input').attr('disabled', true)

      if ($this.is(':not(:checked)')) {
        $( `[${dataTarget}]` ).show().find(':input' ).attr('disabled', false)
      }
    }
  })
}
