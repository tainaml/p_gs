if ( $( '[data-page="courses"]' ).length ) {
  const $sideMenu = $( '[data-target="sidemenu"]' )
  const $dispather = $( '[data-toggle="sidemenu"]' )
  const $showMore = $( '[data-toggle="showmore"]' )
  const ESC_KEYCODE = 27
  const animateMenu = ( position = {
    left: 0
  }) => {
    $sideMenu.animate( position )
    $( 'body' ).toggleClass( 'modal-open' )
  }


  $dispather.on( 'click tap', ( event ) => {
    animateMenu()
  })

  $sideMenu.on( 'click tap', ( event ) => {
    if ( $( event.target ).is( '.side__menu' )) {
      animateMenu({
        left: '100%'
      })
    }
  })

  $( window ).on( 'keydown', ( event ) => {
    if ( event.keyCode == 27 ) {
      animateMenu({
        left: '100%'
      })
    }
  })

  $showMore.on( 'click tap', ( event ) => {
    const $list = $( event.target ).siblings( '.list-unstyled' )
    const $itemList = $list.find( '[data-hidden]' )

    $itemList.toggleClass( function () {
      $( this ).removeClass( 'item__visible item__hidden' )

      if ( $( this ).data( 'hidden' ) ) {
        $( this ).data( 'hidden', false )
        $( event.target ).text( 'Fechar' )
        return 'item__visible'
      } else {
        $( this ).data( 'hidden', true )
        $( event.target ).text( 'mais 10...' )
        return 'item__hidden'
      }
    })
  })

  $sideMenu.prependTo( 'body' )
}
