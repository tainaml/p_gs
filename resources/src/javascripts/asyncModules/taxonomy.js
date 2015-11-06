'use strict';

require('selectize');

import $ from 'jquery';

var taxonomy,
    elementData,
    $element,
    TemplateEngine = require('./TemplateEngine');

var defaultSettings = {
    plugins: ['remove_button'],
    maxItems: 5,
    valueField: 'url',
    labelField: 'name',
    searchField: 'name',
    create: false,
    render: {
        'item': renderItem,
        'option': renderOption
    },
    load: loadItems
};

var defaultTemplates = {
    'item': '<div><%this.name%></div>',
    'option': '<div class="item-float-notification"><span><img src="http://placehold.it/20" alt="<%this.name%>"></span><span><%this.name%></span></div>'
};

function renderItem(item){

    var $element = $(this.$input);
    var renderTemplate = defaultTemplates.item;
    var elementData = $element.data();
    if('templateItem' in elementData && $(elementData.templateItem).length){
        renderTemplate = $(elementData.templateItem).html();
    }

    return TemplateEngine(renderTemplate, item);
}

function renderOption(item, escape){

    var $element = $(this.$input);
    var renderTemplate = defaultTemplates.option;
    var elementData = $element.data();
    if('templateOption' in elementData && $(elementData.templateOption).length){
        renderTemplate = $(elementData.templateOption).html();
    }

    return TemplateEngine(renderTemplate, item);

}

function loadItems(query, callback) {

    var options = $(this.$input).data();

    if(!query.length){
        return callback();
    }

    var _data = {};
    _data[this.settings.searchField] = query;

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

taxonomy = (element) => {
    $element = $(element);
    elementData = $element.data();
    var selectizeSettings = $.extend({}, defaultSettings, elementData);
    $(element).selectize(selectizeSettings);
};

export default taxonomy