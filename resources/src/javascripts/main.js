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

$(() => {
    require('./modules')
    require('perfect-scrollbar/jquery')($);

    $('[data-toggle="custom-scroll"] > .float-notifcations').perfectScrollbar();

    // Modals
    $('[data-target=modal]').modal({ show: false });
    $('[data-toggle=modal]').on('click', function (event) {
        $(this).parents('[data-target=modal]').modal('hide');
    });

});