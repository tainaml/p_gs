module.exports = ( name ) => {
  const $element = $( name )


  $element.on({
    focus: function ( event ) {
      const $this = $( this )
      $this.siblings( 'label' ).addClass( 'active' )
    },
    blur: function ( event ) {
      const $this = $( this )
      if ( !$this.val() ) {
        $this.siblings( 'label' ).removeClass( 'active' )
      }
    }
  })
}
