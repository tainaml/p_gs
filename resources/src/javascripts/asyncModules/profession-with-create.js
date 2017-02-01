'use strict';

require('selectize');

import $ from 'jquery';

var profession,
  elementData,
  $element;

var defaultSettings = {
  create: function ( input ) {
    const detached_responsibility = $( '[data-toggle="detached"]' )
    detached_responsibility.val( input )
    return {
      'value': '',
      'text': input
    };
  },
};

profession = ( element ) => {
  const $element = $( element )
  elementData = $element.data()
  var selectizeSettings = $.extend( {}, defaultSettings, elementData )
  $element.selectize( defaultSettings )
};

export default profession;
