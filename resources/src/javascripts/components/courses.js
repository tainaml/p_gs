import '../vendor/rateYo/jquery.rateyo';
module.exports = ( name ) => {
  const $showMore = $( '[data-toggle="showmore"]' )
  const $rating = $( '[data-toggle="rating"]' )
  const formRating = $( '[data-toggle="rating-value"]' )

  const defaultSettings = {
    halfStar: true,
    normalFill: '#a09e9e',
    ratedFill: '#d68004',
    spacing: '2px',
    starWidth: '20px',
    onSet: function (rating, rateYoInstance) {
      formRating.val( rating )
    },
    onChange: function (rating, rateYoInstance) {
      const reactions = $( rateYoInstance.node ).data( 'reactions' )
      $( this ).next().text( reactions[ Math.floor( rating )])
    }
  }

  $rating.each( ( index, item ) => {
    const $this = $( item )
    const dataConfig = $this.data( 'config' )
    const settings = $.extend({}, defaultSettings, dataConfig)
    $this.rateYo( settings )
  })

  $( '[data-form-send]' ).on( 'change', function onChangeSelectSendVideoForm () {
    var $self = $( this )
    var $form = $self.closest( 'form[data-form-send-enables]' )
    if ( $form.length ) {
      $form.trigger( 'submit' )
    }
  })


  $showMore.on( 'click tap', ( event ) => {
    toggleHeight($( event.currentTarget ).attr( 'href' ))
    event.preventDefault()
  })
  }

  const toggleHeight = ( seletor ) => {
  const $this = $( seletor )
  const ANIMATION_TIME = $this.data( 'animationSpeed' ) || 200

  if ( $this.hasClass( 'open' )) {
    $this.animate({
      height: $this.data( 'height' )
    }, ANIMATION_TIME, () => $this.removeClass( 'open' ))

    return false
  }

  const currentHeight =  $this.outerHeight();
  const autoHeight = $this.css('height', 'auto').outerHeight()
  $this.data('height', currentHeight)
  .height(currentHeight).animate({
    height: autoHeight
  }, ANIMATION_TIME, () => $this.addClass( 'open' ))
}
