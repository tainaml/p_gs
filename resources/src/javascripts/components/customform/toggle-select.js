module.exports = ( select ) => {
  const $select = $( select )
  const $target = $( '[data-salary]' )

  $select.on({
    change: function ( event ) {
      const $this = $( event.currentTarget )
      $target.hide()
      $( `[data-salary=${$this.val()}]` ).show()
    }
  })
}
