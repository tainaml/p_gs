import '../../vendor/rateYo/jquery.rateyo';

if ( $( '[data-page="courses"]' ).length ) {
  const $showMore = $( '[data-toggle="showmore"]' )
  const $rating = $( '[data-toogle="rating"]' )
  const formRating = $( '[name="rating"]' )

  const defaultSettings = {
    rating: 3.6,
    spacing: '5px',
    starWidth: '18px',
    onSet: function (rating, rateYoInstance) {
      formRating.val( rating )
      alert( `Rating is set to: ${rating}` )
      console.log( formRating.val() )
    },
    onChange: function (rating, rateYoInstance) {
      $(this).next().text(rating);
    }
  }

  $rating.each( ( index, item ) => {
    let $this = $( item )
    const dataConfig = $this.data( 'config' )
    const settings = $.extend({}, {
      spacing: '5px',
      starWidth: '18px',
      onSet: function (rating, rateYoInstance) {
        formRating.val( rating )
      },
      onChange: function (rating, rateYoInstance) {
        $(this).next().text(rating);
      }
    }, dataConfig)
    $this.rateYo( settings )
  })



  $showMore.on( 'click tap', ( event ) => {
    toggleHeight($( event.currentTarget ).attr( 'href' ))
    event.preventDefault()

  })
}

const toggleHeight = ( seletor ) => {
  const $this = $( seletor )
  const ANIMATION_TIME = $this.data('animationSpeed') || 200

  if ( $this.hasClass( 'open' )) {
    $this.animate({
      height: $this.data( 'height' )
    }, 200, function () {
      $this.removeClass( 'open' )
    })

    return false
  }

  const currentHeight =  $this.height();
  const autoHeight = $this.css('height', 'auto').height()
  $this.data('height', currentHeight)
  .height(currentHeight).animate({
    height: autoHeight
  }, ANIMATION_TIME,
  function () {
    $this.addClass( 'open' )
  })
}
