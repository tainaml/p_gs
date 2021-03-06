'use strict';

// import $ from 'jquery';
require('selectize');


var profession,
  elementData,
  $element;

var defaultSettings = {
  create: function ( input, callback ) {
    const detached_responsibility = $( '[data-toggle="detached"]' )
    detached_responsibility.val( input )

    callback({
      'value': '',
      'text': detached_responsibility.val()
    })
  },
  render: {
    option_create: function ( create ) {
      return `<div class="create">${create.input}</div>`
    }
  }
};

profession = ( element ) => {
  const $element = $( element )
  elementData = $element.data()
  var selectizeSettings = $.extend( {}, defaultSettings, elementData )
  $element.selectize( defaultSettings )
};

export default profession;
