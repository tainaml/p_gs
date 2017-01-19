module.exports = ( name ) => {
  const $element = $( name )

  $element.map( element => {
    if ( $element[element].nodeName === 'TEXTAREA' && ( $element[element].value.length !== 0 )) {
      setTimeout( inputResize( $element[element] ), 0)
    }
  })

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
    },
    input: function ( event ) {
      if ( event.currentTarget.nodeName === 'TEXTAREA' ) {
        setTimeout( inputResize( event.currentTarget ), 0)
      }
    }
  })
}

const inputResize = ( selector ) => {
  const style = selector.style
  style.height = 'auto'
  style.height = selector.scrollHeight+'px'
}
