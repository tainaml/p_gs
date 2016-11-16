'use strict';

import $ from 'jquery';
import 'jscroll';

if ( $( '[data-page="videos"]' ).length) {
  $( '.j-scroll' ).jscroll({
      autoTrigger: false,
      loadingHtml: '<div class="col-xs-12"><div class="load-async-preload"></div></div>',
      contentSelect: '.j-scroll-container',
      nextSelector: 'a[data-jscroll-next]'
  });

  $( '[data-form-send]' ).on( 'change', function onChangeSelectSendVideoForm () {
    var $self = $(this);
    var $form = $self.closest( 'form[data-form-send-enables]' );
    if ( $form.length ) {
        $form.trigger('submit');
    }
  });
}
