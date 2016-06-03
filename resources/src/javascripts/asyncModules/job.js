'use strict';

require('selectize');

import $ from 'jquery';

var job,
  elementData,
  $element;

var defaultSettings = {
  plugins: ['remove_button'],
  delimiter: ',',
  persist: false,
  create: true,
  render: {
    option_create: function (item) {
      console.log(item);
      return `<div class="create">${item.input}</div>`;
    }
  }
};

job = (element) => {
  $element = $(element);
  elementData = $element.data();
  // var selectizeSettings = $.extend({}, defaultSettings, elementData);
  $(element).selectize(defaultSettings);
};

export default job;
