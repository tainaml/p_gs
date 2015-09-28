require('./vendor/bootstrap/')
require('malihu-custom-scrollbar-plugin')($)
const Dropzone = require('dropzone')
const Selectize = require('selectize')
$(() => {
    require('./modules')
    $('#modal-personal-infos').modal('show')

    // Modals
    $('[data-target=modal]').modal({ show: false })
    $('[data-toggle=modal]').on('click', function (event) {
        $(this).parents('[data-target=modal]').modal('hide')
    })

    // custom file uploads
    var gstiDropzone = new Dropzone('[data-toggle="dropzone"]', {
        url: 'profile',
        maxFiles: 1
    })
    gstiDropzone.on('addedfile', function (file) {
        $('.dz-default.dz-message').hide()
    })
    .on("maxfilesexceeded", function(file) {
        this.removeFile(file);
    });

    // Custom scroll
    $('[data-toggle="custom-scroll"]').mCustomScrollbar()

    // Custom tags
    $('[data-toggle="selectize"]').Selectize();
})