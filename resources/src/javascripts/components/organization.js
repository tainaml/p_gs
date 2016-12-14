module.exports = ( name ) => {
  const $root = $( name )

  const $input = $root.find( 'input:text' ) // TODO: Change selector
  const $tab = $root.find( '[data-toggle="tab"]' )

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

    const tabContent = $( '[role=tabpanel]' )
    const $this = $( event.currentTarget )
    const target =  $this.attr('href')

    $this.addClass( 'active' )
    tabContent.fadeOut(() => {
      $( target ).fadeIn()
    })
  })
};
