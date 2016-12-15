module.exports = ( name ) => {
  const $root = $( name )

  const $input = $root.find( 'input:text' ) // TODO: Change selector
  const $tab = $root.find( '[data-toggle="tab"]' )
  const $tabContent = $( '[role=tabpanel]' )

  $tabContent.not( '.active' ).hide()

  $input.on( 'focus', ( event ) => {
    const $this = $( event.currentTarget )
    $this.closest( '.organization__form__item' ).addClass( 'active' )
  })
  .on( 'blur', ( event ) => {
    const $this = $( event.currentTarget )
    $this.closest( '.organization__form__item' ).removeClass( 'active' )

  })

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
