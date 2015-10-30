'use strict'

import $ from 'jquery'
require('selectize')

const [suggest] = [{
    plugins: ['remove_button']
    , maxItems: 5
    , valueField: 'url'
    , labelField: 'name'
    , searchField: 'name'
    , create: false
    , render: {
        item: templateItem
        , option: templateOption
    }
    , load: loadUsers
}]

var tagger = (element) => {
    var type = $(element).data('taggerType');
    switch (type) {
        case 'suggest':
            $(element).selectize(suggest)
    }
}

function templateItem(item, escape) {
    let name = item.name ? escape(item.name) : '';
    return `<div>${name}</div>`
}
function templateOption(item, escape) {
    let name = item.name ? escape(item.name) : '';
    return `<div class="item-float-notification">
    <span><img src="http://placehold.it/20" alt="${name}"></span>
    <span>${name}</span>
  </div>`
}

function loadUsers(query, callback) {
    var options = this.$wrapper.prev().data();
    if (!query.length) {
        return callback()
    }
    $.ajax({
        url: options.url,
        type: 'GET',
        data: {
            criteria: query
        },
        error: function () {
            callback()
        },
        success: function (res) {
            console.dir(res.users);
            console.log(res);
            callback(res.users)
        }
    })
}


export default tagger