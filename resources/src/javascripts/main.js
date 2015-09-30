import './asyncModules'

require('./vendor/bootstrap/')
// require('malihu-custom-scrollbar-plugin')($)
// const Selectize = require('selectize')
$(() => {
    require('./modules')
    $('#modal-personal-infos').modal('show')

    // Modals
    $('[data-target=modal]').modal({ show: false })
    $('[data-toggle=modal]').on('click', function (event) {
        $(this).parents('[data-target=modal]').modal('hide')
    })

    // Custom scroll
    // $('[data-toggle="custom-scroll"]').mCustomScrollbar()

    // Custom tags
    // $('[data-toggle="selectize"]').Selectize();
})