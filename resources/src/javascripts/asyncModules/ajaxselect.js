'use strict'

// import $ from 'jquery'
require('selectize')

var elementData,
    $element;

const [suggest] = [{
    valueField: 'id'
    , labelField: 'name'
    , searchField: 'name'
    , create: false
    , highlight: false
    , render: {
        item: templateItem
        , option: templateOption
    }
    , load: loadUsers
}]

var ajaxselect = (element) => {
    $element = $(element);
    elementData = $element.data();
    var selectizeSettings = $.extend({}, suggest, elementData);
    $(element).selectize(selectizeSettings);
}

function templateItem (item, escape) {
    let name = item.name ? escape(item.name) : ''
    return `<div>${name}</div>`
}
function templateOption (item, escape) {
    let name = item.name ? escape(item.name) : ''
    let template = `<div class="item-float-notification">
      <span><img src="${item.img}" alt="${name}"></span>
      ${name}
    </div>`
    return template
}

function loadUsers ( query, callback ) {
    const options = this.$wrapper.prev().data();
    const _data = {};

    if (!query.length) {
      return callback()
    }

    _data[this.settings.searchField] = query;
    console.log(_data);

    $.ajax({
        url: options.url,
        type: 'GET',
        data: _data,
        error: function () {
          callback()
        },
        success: function (res) {
          callback(res.items);
        }
    })
}


export default ajaxselect
