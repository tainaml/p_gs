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
  // create: true,
  // render: {
  //   option_create: function (item) {
  //     return `<div class="create">${item.input}</div>`;
  //   }
  // }
};

profession = ( element ) => {
  const $element = $( element )
  console.log($element);
  elementData = $element.data()
  var selectizeSettings = $.extend( {}, defaultSettings, elementData )
  $element.selectize( defaultSettings )
};

export default profession;
