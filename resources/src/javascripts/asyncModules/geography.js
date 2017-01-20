'use strict';

require('selectize');

import $ from 'jquery';

var profession,
  elementData,
  $element;

var defaultSettings = {
  plugins: ['remove_button'],
  // delimiter: ',',
  // persist: false,
  create: true,
  render: {
    item: function (item) {
      return `<div>${item.input}</div>`;
    },
    option: function (item) {
      return `<div>${item.input}</div>`;
    }
  },
  load: function (query, callback) {
    var options = $(this.$input).data();

    if(!query.length){
        return callback();
    }

    var _data = {};
    _data[this.settings.searchField] = query;
    console.log(_data);

    $.ajax({
        url: options.url,
        data: _data,
        type: options.method || 'GET',
        error: function(){
            callback()
        },
        success: function(res){
            callback(res);
        }
    });
  }
};

profession = ( element ) => {
  const $element = $( element )
  elementData = $element.data()
  var selectizeSettings = $.extend( {}, defaultSettings, elementData )
  $element.selectize( defaultSettings )
};

export default profession;
