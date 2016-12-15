import input from './customform/input'

module.exports = ( name ) => {
  const $root = $( name )

  input( $root.find( '[data-toggle="input"]' )) // TODO: Change selector
  const $tab = $root.find( '[data-toggle="tab"]' )
  const $tabContent = $( '[role=tabpanel]' )

  $tabContent.not( '.active' ).hide()

  $tab.on( 'click tap', '[role=tab]', ( event ) => {
    event.preventDefault()

    const $this = $( event.currentTarget )
    const target =  $this.attr('href')

    $this.addClass( 'active' )
    $tabContent.fadeOut(() => {
      $( target ).fadeIn()
    })
  })
};
