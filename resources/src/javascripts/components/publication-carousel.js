import 'slick-carousel'
import '../vendor/rateYo/jquery.rateyo'

const defaultRate = {
  halfStar: true,
  normalFill: '#a09e9e',
  ratedFill: '#d68004',
  spacing: '2px',
  starWidth: '20px'
}

module.exports = ( mod ) => {
  const $rating = $( '[data-toggle="rating"]' )

  $( mod ).slick({
    slidesToShow: 4,
    slidesToScroll: 4,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 3
        }
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        }
      }
    ]
  })

  $rating.each( ( index, item ) => {
    const $this = $( item )
    const dataConfig = $this.data( 'config' )
    const settings = $.extend({}, defaultRate, dataConfig)
    $this.rateYo( settings )
  })
}
