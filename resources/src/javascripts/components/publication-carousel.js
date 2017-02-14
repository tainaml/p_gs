import '../vendor/jquery.jcarousel'
import '../vendor/rateYo/jquery.rateyo'

const defaultRate = {
  halfStar: true,
  normalFill: '#a09e9e',
  ratedFill: '#d68004',
  spacing: '2px',
  starWidth: '20px'
}

module.exports = ( mod ) => {
  const $rating = $( '[data-toggle="rating"]' );
  const $module = $( mod );

  $module
    .on('jcarousel:reload jcarousel:create', function () {
      var carousel = $( this ),
      width = carousel.innerWidth();

      if (width > 768) {
        width = width / 4;
      } else if (width < 768 && width > 480 ) {
        width = width / 2;
      } else if (width <= 480) {
        width = width;
      }

      carousel.jcarousel('items').css('width', Math.ceil(width) + 'px');
    }).jcarousel({
      wrap: 'circular'
    });

    $('.jcarousel-control-prev').jcarouselControl({
      target: '-=1'
    });

    $('.jcarousel-control-next').jcarouselControl({
      target: '+=1'
    });

  $rating.each( ( index, item ) => {
    const $this = $( item )
    const dataConfig = $this.data( 'config' )
    const settings = $.extend({}, defaultRate, dataConfig)
    $this.rateYo( settings )
  })
}
