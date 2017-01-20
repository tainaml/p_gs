'use strict';

require('selectize');

import $ from 'jquery';

let geography,
  elementData,
  $element;

var defaultSettings = {
  plugins: ['remove_button'],
  maxItems: null,
  valueField: 'name',
  labelField: 'name',
  searchField: 'name',
  options: [],
  create: false,
  render: {
    item: function (item) {
      console.log(item);
      return `<div>${item.name}</div>`;
    },
    option: function (option, escape) {
      console.dir(option);
      return `<div>${escape(option.name)}</div>`;
    }
  },
  load: function (query, callback) {
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
        success: function(res){
            // console.log(res)
            // console.dir( result )
            callback( res )
        }
    });
  }
};

geography = ( element ) => {
  const $element = $( element )
  elementData = $element.data()
  var selectizeSettings = $.extend( {}, defaultSettings, elementData )
  $element.selectize( defaultSettings )
//   $element.selectize({
//     valueField: 'url',
//     labelField: 'name',
//     searchField: 'name',
//     create: false,
//     render: {
//       option: function(item, escape) {
//           return '<div>' +
//               '<span class="title">' +
//                   '<span class="name"><i class="icon ' + (item.fork ? 'fork' : 'source') + '"></i>' + escape(item.name) + '</span>' +
//                   '<span class="by">' + escape(item.username) + '</span>' +
//               '</span>' +
//               '<span class="description">' + escape(item.description) + '</span>' +
//               '<ul class="meta">' +
//                   (item.language ? '<li class="language">' + escape(item.language) + '</li>' : '') +
//                   '<li class="watchers"><span>' + escape(item.watchers) + '</span> watchers</li>' +
//                   '<li class="forks"><span>' + escape(item.forks) + '</span> forks</li>' +
//               '</ul>' +
//           '</div>';
//       }
//     },
//     score: function(search) {
//         var score = this.getScoreFunction(search);
//         return function(item) {
//             return score(item) * (1 + Math.min(item.watchers / 100, 1));
//         };
//     },
//     load: function(query, callback) {
//         if (!query.length) return callback();
//         $.ajax({
//             url: 'https://api.github.com/legacy/repos/search/' + encodeURIComponent(query),
//             type: 'GET',
//             error: function() {
//                 callback();
//             },
//             success: function(res) {
//               console.log(res.repositories);
//                 callback(res.repositories.slice(0, 10));
//             }
//         });
//     }
// });
};

export default geography;
