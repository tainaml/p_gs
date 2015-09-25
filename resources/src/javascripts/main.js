require('./vendor/bootstrap/');
$(() => {

    $('#modal-personal-infos').modal('show');

    // Modals
    $('[data-target=modal]').modal({ show: false });
    $('[data-toggle=modal]').on('click', function (event) {
        $(this).parents('[data-target=modal]').modal('hide');
    })
});