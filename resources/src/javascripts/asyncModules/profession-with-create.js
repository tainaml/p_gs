'use strict';

require('selectize');

import $ from 'jquery';

var profession,
  elementData,
  $element;

var defaultSettings = {
  // plugins: ['remove_button'],
  // delimiter: ',',
  // persist: false,
  create: function ( input ) {
    const detached_responsibility = $( '[name="detached_responsibility"]' )
    detached_responsibility.val( input )
  },
  // render: {
  //   option_create: function (item) {
  //     return `<div class="create">${item.input}</div>`;
  //   }
  // }
};

profession = ( element ) => {
  const $element = $( element )
  elementData = $element.data()
  var selectizeSettings = $.extend( {}, defaultSettings, elementData )
  $element.selectize( defaultSettings )
};

export default profession;
