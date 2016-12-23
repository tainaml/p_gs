'use strict'

import $ from 'jquery'
require('selectize')

var elementData,
    $element;

const [suggest] = [{
    valueField: 'id'
    , labelField: 'name'
    , searchField: 'name'
    , create: false
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
    return `<div class="item-float-notification">
        <span><img src="${item.img}" alt="${name}"></span>
        <span>${name}</span>
        </div>`
}

function loadUsers(query, callback) {
    var options = this.$wrapper.prev().data();
    if (!query.length) {
        return callback()
    }

    var _data = {};
    _data[this.settings.searchField] = query;

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