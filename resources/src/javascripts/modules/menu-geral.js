;(function () {
  'use strict';
  var $header = $('.js-navigation');
  var $toggle_categories = $('.toggle_menu-categories');
  var showHeaderMenu = function (event) {
    $header.toggleClass('is-oppened');
    return false;
  }

  $toggle_categories.on('click', showHeaderMenu);
})();
