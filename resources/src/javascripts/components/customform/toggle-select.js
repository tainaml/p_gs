module.exports = ( select, dataTarget ) => {
  const $select = $( select )
  const $target = $( `[${dataTarget}]` )
  $target.hide()
  $target.find(':input').attr('disabled', true)
  $( `[${dataTarget}=${$select.val()}]` ).show().find(':input' ).attr('disabled', false)

  $select.on({
    change: function ( event ) {
      const $this = $( event.currentTarget )
      $target.hide()
      $target.find(':input').attr('disabled', true)
      $( `[${dataTarget}=${$this.val()}]` ).show().find(':input' ).attr('disabled', false)
    }
  })
}
