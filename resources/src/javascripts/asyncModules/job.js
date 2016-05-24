'use strict';

require('selectize');

import $ from 'jquery';

var job,
    elementData,
    $element;

var defaultSettings = {
    delimiter: ',',
    persist: false,
    create: function(input) {
        return {
            value: input,
            text: input
        }
    }
};

job = (element) => {
    $element = $(element);
    elementData = $element.data();
    var selectizeSettings = $.extend({}, defaultSettings, elementData);
    $(element).selectize(selectizeSettings);
};

export default job