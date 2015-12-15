'use strict';

import 'jscroll'
import './asyncModules'
import './vendor/bootstrap/'
import './modules/ideiaForm/'
import './modules/ideiaAsyncSocialAction/'
import './modules/ideiaAutocomplete/'
import './modules/ideiaLoadAsync/'
import './modules/ideiaCounter/'
<<<<<<< HEAD
import './modules/ideiaFilter/'
=======
import './modules/ideiaLogin/'
>>>>>>> 11b2eb7271a2b85183ea0504afa92b6264a36cf5

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