'use strict';

// import $ from 'jquery';
require('selectize');


var profession,
  elementData,
  $element;

var defaultSettings = {};

profession = ( element ) => {
  const $element = $( element )
  elementData = $element.data()
  var selectizeSettings = $.extend( {}, defaultSettings, elementData )
  $element.selectize( defaultSettings )
};

export default profession;
