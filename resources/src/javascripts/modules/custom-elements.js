// Custom dropdown
$('.custom-select-item').on('click', showChilds);
function showChilds (event) {
    event.preventDefault();
    if ($(this).next('.custom-select-list').is(':visible')) {
        return false;
    }
    $('.custom-select-list').slideUp();
    $(this).next('.custom-select-list').slideDown();
    return false;
}

$('.custom-select-option').on('click', setDropValue);
function setDropValue (event) {
    event.preventDefault();
    let value = $(this).data('value');
    console.log(value);
}
$(document).on('click', function () {
    if ($('.custom-select-list:visible')) {
        $('.custom-select-list').slideUp();
    }
});