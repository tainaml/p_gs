module.exports = ( select ) => {
  const $select = $( select )
  const $target = $( '[data-salary]' )
  $target.hide()

  $select.on({
    change: function ( event ) {
      const $this = $( event.currentTarget )
      $target.hide()
      $target.find(':input').attr('disabled', true)
      $( `[data-salary=${$this.val()}]` ).show().find(':input' ).attr('disabled', false)
    }
  })
}
