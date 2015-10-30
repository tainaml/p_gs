'use strict'

import './asyncModules'

require('./vendor/bootstrap/')
require('./modules/ideiaForm/')
require('./modules/ideiaAsyncSocialAction/')

$(() => {
    // require('malihu-custom-scrollbar-plugin')($)
    require('./modules')
    $('#modal-personal-infos').modal('show')
    // $('#modal-sugerir').modal('show')

    // Modals
    $('[data-target=modal]').modal({ show: false })
    $('[data-toggle=modal]').on('click', function (event) {
        $(this).parents('[data-target=modal]').modal('hide')
    })

    // Custom tags
    // $('[data-toggle="selectize"]').Selectize()
})