$(function onReadyToSelectize(){

    $('[data-ideia-selectize]').each(function eachSelectizeElement(){

        var $element = $(this);

        $element.selectize({
            create: false,
            valueField: 'value',
            labelField: 'label',
            searchField: 'label',
            //render: {
            //    option: function onSelectizeRenderOption(data, escape){
            //        return '<div>' + data.label + '</div>';
            //    },
            //    item: function(data, escape){
            //        return '<div>' + data.label + '</div>';
            //    }
            //},
            load: function onSelectizeLoad(query, callback){

                if(query.length < 3){
                    return callback();
                }

                $.ajax({
                    url: $element.data('url'),
                    type: 'GET',
                    dataType: 'json',
                    data: {
                        q: query
                    },
                    error: function onSelectizeAjaxError(){
                        console.log('Erro ao tentar carregar informações para esse campo: ' + $element.attr('name'))
                    }
                }).done(function onSelectizeAjaxSuccess(data){
                    console.dir(data);
                    console.log('items' in data);
                    console.dir(callback);
                    if('items' in data){
                        callback(data.items)
                    }
                });

            }
        });

    });

});