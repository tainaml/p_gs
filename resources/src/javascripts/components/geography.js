'use strict';

require('selectize');

import $ from 'jquery';

let defaultSettings = {
  plugins: ['remove_button'],
  maxItems: null,
  valueField: 'id',
  labelField: 'name',
  searchField: 'name',
  options: [],
  create: false,
  render: {
    item: function (item) {
      return `<div>${item.name}</div>`;
    },
    option: function (option, escape) {
      return `<div>${escape(option.name)}</div>`;
    }
  },
  load: function ( query, callback ) {
    var options = $(this.$input).data();

    if(!query.length){
        return callback();
    }

    var _data = {};
    _data[this.settings.searchField] = query;

    $.ajax({
        url: options.url,
        data: _data,
        dataType: 'json',
        type: options.method || 'GET',
        error: function(){
            callback()
        },
        success: function ( res ) {
            callback( res )
        }
    });
  }
};

const geography = ( element ) => {
  const $element = $( element )
  const elementData = $element.data()
  const selectizeSettings = $.extend( {}, defaultSettings, elementData )
  $element.selectize( defaultSettings )
};

export default geography;
