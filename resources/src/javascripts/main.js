'use strict'

import './asyncModules'

require('./vendor/bootstrap/')
require('./modules/ideiaForm/')
require('./modules/ideiaAsyncSocialAction/')

$(() => {
    require('./modules')
    $('#modal-personal-infos').modal('show');

    // Modals
    $('[data-target=modal]').modal({ show: false });
    $('[data-toggle=modal]').on('click', function (event) {
        $(this).parents('[data-target=modal]').modal('hide');
    });

});