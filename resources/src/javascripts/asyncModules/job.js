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
      return `<div class="create">${item.input}</div>`;
    }
  }
};

job = (element) => {
  $element = $(element);
  elementData = $element.data();
  $(element).selectize(defaultSettings);
};

export default job;
