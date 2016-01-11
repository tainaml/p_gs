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


function affixBoxShare() {

    var $box = $('.box-share');
    var $post = $('.full-post');
    var $window = $(window);

    var boxHeight = $box.outerHeight();
    var boxPadding = 20;
    var boxInitialTop = $box.offset().top;
    var boxOffsetTopFixed = $box.offset().top - boxPadding;

    var postHeight = $post.outerHeight();
    var postOffsetBottom = $post.offset().top + postHeight;

    var scrollize = function() {

        if (postHeight != $post.outerHeight()) {
            postHeight = $post.outerHeight();
            postOffsetBottom = $post.offset().top + postHeight;
        }

        if ($window.scrollTop() >= boxOffsetTopFixed) {
            if (!$box.hasClass('fixed')) {
                $box.addClass('fixed').css({
                    'position': 'fixed',
                    'top': boxPadding
                });
            } else {
                if (($window.scrollTop() + $box.outerHeight() + boxPadding) < postOffsetBottom) {
                    if ($box.hasClass('fixed-relative')) {
                        $box.removeClass('fixed-relative').css({
                            'position': 'fixed',
                            'top': boxPadding
                        });
                    }
                } else {
                    if (!$box.hasClass('fixed-relative')) {
                        $box.addClass('fixed-relative').css({
                            'position': 'absolute',
                            'top': postOffsetBottom - boxHeight
                        });
                    }
                }
            }
        } else {
            if ($box.hasClass('fixed')) {
                $box.removeClass('fixed').css({
                    'position': 'absolute',
                    'top': boxInitialTop
                });
            }
        }
    };

    $(window).scroll(scrollize);
    $(window).load(scrollize)
}

if ($('.box-share').length && $('.full-post').length) {
    affixBoxShare();
}