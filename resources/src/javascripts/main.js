'use strict';

import 'jscroll'
import './asyncModules'
import './vendor/bootstrap/'
import './modules/ideiaForm/'
import './modules/ideiaAsyncSocialAction/'
import './modules/ideiaAutocomplete/'
import './modules/ideiaLoadAsync/'
import './modules/ideiaCounter/'
import './modules/ideiaFilter/'
import './modules/ideiaLogin/'
import './modules/ideiaNotification/'
import './modules/ideiaRestrict/'
import './modules/ideiaValidationField/'
import Slideout from 'slideout'

$(() => {
    require('./modules');
    require('perfect-scrollbar/jquery')($);

    $('[data-toggle="custom-scroll"] > .float-notifcations').perfectScrollbar();

    // Modals
    $('[data-target=modal]').modal({ show: false });
    $('[data-toggle=modal]').on('click', function (event) {
        $(this).parents('[data-target=modal]').modal('hide');
    });

    // Tooltips
    $('[data-toggle=tooltip]').tooltip();

    // Slideout
    var slideout = new Slideout({
        'panel': document.getElementById('wrapper'),
        'menu': document.getElementById('slideout-menu'),
        'padding': 256,
        'tolerance': 70
    });
    $(document).on('click', '.toggle-slideout', function() {
        slideout.toggle();
    });
    var mobileSearch = $('#mobile-search');
    $('.toggle-search').on('click', function(e) {
        e.preventDefault();
        mobileSearch.slideToggle();
    });
});