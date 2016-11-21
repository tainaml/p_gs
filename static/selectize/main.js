$(function onReadyToSelectize(){

    $('[data-ideia-selectize]').each(function eachSelectizeElement(){

        var $element = $(this);

        $element.selectize({
            create: false
        });

    });

});