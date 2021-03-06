require('./when-event.js');
require('./validation.js');

(function($){
    'use strict';

    $.fn.IdeiaAjaxForm = function(action){

        var defaultOptions = {
            'groupClass': '.form-group'
        };

        var EVENT_AJAX_VALIDATION = 'ajaxform.validation';

        function addError(field, error, unique){
            var isUnique = unique || false;
            var $target;

            if(this instanceof Event){
                $target = $(this.currentTarget);
            }else{
                $target = $(this);
            }

            var errors = $target.data('formErrors');

            if(!(field in errors) || isUnique){
                errors[field] = [];
            }

            errors[field].push(error);
            $target.data('form-errors', errors);
        }

        function formCancelSubmit(e){
            e.preventDefault();
            var $self = $(this);

            $self.one(EVENT_AJAX_VALIDATION, doValidation);
            $self.on('ajaxform.error', function doAjaxFormErrosShow(event, data){
                if('errors' in data){
                    doShowErrors.call(this, data.errors);
                }else{
                    console.error(data);
                }
            });

            $self.whenEvent(EVENT_AJAX_VALIDATION).done(afterValidation);

            $self.find('.has-error').removeClass('has-error');
            $self.find('.form-group-errors').empty();

            var formFields = $self.data('formFields');
            $.each(formFields, function __eachFieldInFormFields(key){
                var $field = formFields[key]['object'];
                var $group = formFields[key]['group'];

                $group.find('.has-error').removeClass('has-error');
                $group.find('.form-group-errors').empty();
            });

            $self.data('formFields', formFields);

            $self.data('ajaxFormEnabled', true);
            $self.data('formErrors', {});

            $self.trigger(EVENT_AJAX_VALIDATION, addError);
        }

        function hasErrors(errors){
            var counter = 0;
            for(var item in errors){
                counter++;
            }
            return counter > 0;
        }

        function doValidation(event, addError){
            // addError.call(event, 'fieldname', 'error message', bol_only_this_error)
            // addError.call(event, 'birthday', 'error message', false);
        }

        function afterValidation(){
            var $self = $(this),
                errors = $self.data('formErrors');

            if(hasErrors(errors)){
                doShowErrors.call(this, errors);
            }else{
                doSubmit.call(this);
            }
        }

        function doShowErrors(errors){

            var otherErrors = [];
            var $self = $(this);
            var error, errorText;
            var formFields = $(this).data('formFields');
            var $field, $group;

            if(!errors){
                errors = [];
            }

            $.each(errors, function __eachErrorInErrors(key, values){

                try{

                    if(!(key in formFields)){

                        $.each(values, function addErrorToOtherErrors(){
                            otherErrors.push(this);
                        });

                    }else{
                        $field = formFields[key]['object'];
                        $group = formFields[key]['group'];

                        $group.addClass('has-error');
                        var $errorContainer = $group.find('.form-group-errors');
                        if(!$errorContainer.length){
                            $errorContainer = $('<ul class="form-group-errors"></ul>').appendTo($group);
                        }

                        $errorContainer.empty();

                        for(var i in values){
                            $errorContainer.append($('<li>' + values[i] + '</li>'));
                        }
                    }

                }catch(err){
                    console.dir(err);
                }
            });
        }

        function doSubmit(){

            var $self = $(this);
            var dataType = $self.attr('data-type') || 'json';
            var url = $self.attr('action') || location.href;
            var withFiles = ($self.attr('enctype') === 'multipart/form-data');
            var method = $self.attr('method') || 'post';

            var ajaxParams = {
                'type': method.toUpperCase(),
                'url': url,
                'cache': false,
                beforeSend: function (jqXHR) {
                    $self.find('button[type=submit]').prop('disabled', true);
                    $self.trigger('ajaxform.before-send', jqXHR);
                },
                success: function (data) {
                    $self.trigger('ajaxform.success', data);
                },
                complete: function() {
                    $self.find('button[type=submit]').prop('disabled', false);
                },
                error: function(jqXHR){
                    var data;
                    try {
                        try {
                            data = $.parseJSON(jqXHR.responseText);
                        } catch (e) {
                            if (typeof jqXHR.responseText == 'string') {
                                data = {
                                    'errormessage': jqXHR.responseText
                                };
                            }
                        }
                    } catch (e) {
                        console.log("Can't parse to JSON. Check the response data and contentType");
                        return;
                    }
                    try {
                        $self.trigger('ajaxform.error', [data]);
                    } catch (e) {
                        console.log("Can't add error");
                        console.dir(data);
                        console.dir(e);
                        return false;
                    }

                },
                dataType: dataType,
                data: $self.serialize()
            };

            if(withFiles){
                if(!('FormData' in window)){
                    // Use fake ajax. This browser dont support FormData
                    fakeAjax($self, url)
                }

                ajaxParams.contentType = false;
                ajaxParams.processData = false;
                ajaxParams.data = new FormData(this);
            }

            $.ajax(ajaxParams);
        }

        function fakeAjax($self, url){

            var targetId = 'fakeframex_' + $.now() + Math.random();

            var $iframe = $('<iframe></iframe>');
            $iframe.attr('src', 'about:blank');
            $iframe.attr('id', targetId).attr('name', targetId);
            $iframe.appendTo($('body'));

            $self.off();
            $self.attr('target', targetId);
            $iframe.on('load', function __fakeAjaxOnLoadIFrame(){
                var data = false;
                $self.IdeiaAjaxForm();

                try{
                    data = $.parseJSON($iframe.contents().text());
                    if('error' in data){
                        $self.trigger('ajaxform.success', data);
                    }else{
                        $self.trigger('ajaxform.error', [data]);
                    }

                }catch(err){
                    $self.trigger('ajaxform.error', [{'error': 'Generic Error'}]);
                }
                $iframe.remove();
            });

            $self.trigger('submit');

        }

        function setup(){
            var $self = $(this);
            colectFields.call(this);
            $self.on('submit', formCancelSubmit);
        }

        function colectFields(){

            var fields = {};
            var $self = $(this),
                $object, $group, field, objectKey;

            var $formGroup = $self.data('groupClass') || defaultOptions.groupClass;

            var tempFields = $self.find(':input');

            $.each(tempFields, function forEachFieldInFields(){

                $object = $(this);

                objectKey = $object.attr('name') || false;

                if(!objectKey){
                    return;
                }

                $formGroup = $object.data('groupClass') || $formGroup;
                $group = $object.closest($formGroup);

                field = {
                    'object': $object,
                    'group': $group
                };

                fields[objectKey] = field;
            });

            $self.data('formFields', fields);
        }

        $(this).each(function __eachAjaxFormInPage(){
            setup.call(this);
        });

    };

    function ideiaFormOnReady(){
        var ajaxForms = $(document).find('form[data-ajaxform]');
        ajaxForms.IdeiaAjaxForm();
    }

    $(document).ready(ideiaFormOnReady);


})(jQuery);
