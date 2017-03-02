module.exports = ( name ) => {
  const $element = $( name )

  $element.map( element => {
    if ( $element[element].nodeName === 'TEXTAREA' && ( $element[element].value.length !== 0 )) {
      setTimeout( inputResize( $element[element] ), 0)
    }
  })

  if ( $element.val() ) {
    $element.siblings( 'label' ).addClass( 'active' )
  }

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
  const height = !!selector.scrollHeight ? selector.scrollHeight + 'px' : 'auto'
  style.height = 'auto'

  style.height = height
}
