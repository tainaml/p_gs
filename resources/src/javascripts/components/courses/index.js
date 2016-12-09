import '../../vendor/rateYo/jquery.rateyo';

if ( $( '[data-page="courses"]' ).length ) {
  const $showMore = $( '[data-toggle="showmore"]' )
  const $rating = $( '[data-toogle="rating"]' )
  const formRating = $( '[name="rating"]' )

  const defaultSettings = {
    spacing: '5px',
    starWidth: '18px',
    onSet: function (rating, rateYoInstance) {
      formRating.val( rating )
    },
    onChange: function (rating, rateYoInstance) {
      const reactions = $( rateYoInstance.node ).data( 'reactions' )
      $( this ).next().text( reactions[ Math.ceil( rating ) - 1 ]);
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
