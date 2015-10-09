require('./when-event.js');
require('./validation.js');

(function($){
    'use strict';

    $.fn.IdeiaAjaxForm = function(action){

        var defaultOptions = {
            'groupClass': '.form-group'
        };

        var EVENT_AJAX_VALIDATION = 'ajaxform.validation';

        function formCancelSubmit(e){
            e.preventDefault();
            var $self = $(this);

            $self.one(EVENT_AJAX_VALIDATION, doValidation);

            $self.whenEvent(EVENT_AJAX_VALIDATION).done(afterValidation);

            $self.find('.has-error').removeClass('has-error');
            $self.find('.form-group-errors').children().remove();
            $self.data('ajaxFormEnabled', true);
            $self.data('formErrors', {});

            $self.trigger(EVENT_AJAX_VALIDATION, function _addError(field, error, unique){
                var isUnique = unique || false;
                var event = this;
                var $target = $(event.currentTarget);
                var errors = $target.data('formErrors');

                if(!(field in errors) || isUnique){
                    errors[field] = [];
                }

                errors[field].push(error);
                $target.data('form-errors', errors);
            });
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

            $.each(errors, function(key, values){

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

                    for(var i in values){
                        $errorContainer.append($('<li>' + values[i] + '</li>'));
                    }
                }
            });
        }

        function doSubmit(){

            var $self = $(this);
            var url = $self.attr('action') || location.href;
            var withFiles = ($self.attr('enctype') === 'multipart/form-data');

            var ajaxParams = {
                'type': 'POST',
                'url': url,
                'cache': false,
                'success': function(data){
                    $self.trigger('formajax:success', data);
                },
                'error': function(jqXHR){
                    var data = $.parseJSON(jqXHR.responseText);
                    $self.trigger('formajax:error', [data]);
                },
                'dataType': 'json',
                'data': $self.serialize()
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
            $iframe.on('load', function(){
                var data = false;
                $self.IdeiaAjaxForm();

                try{
                    data = $.parseJSON($iframe.contents().text());
                    if('error' in data){
                        $self.trigger('formajax:success', data);
                    }else{
                        $self.trigger('formajax:error', [data]);
                    }

                }catch(err){
                    $self.trigger('formajax:error', [{'error': 'Generic Error'}]);
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
                $object, $group, field;

            var $formGroup = $self.data('groupClass') || defaultOptions.groupClass;

            var tempFields = $self.serializeArray();
            $.each(tempFields, function forEachFieldInFields(){

                $object = $self.find('[name=' + this.name + ']');
                $formGroup = $object.data('groupClass') || $formGroup;
                $group = $object.closest($formGroup);

                field = {
                    'object': $object,
                    'group': $group
                };

                fields[this.name] = field;
            });

            $self.data('formFields', fields);

        }

        $(this).each(function(){
            setup.call(this);
        });

    };

    function ideiaFormOnReady(){
        var ajaxForms = $('form[data-ajaxform]');
        ajaxForms.IdeiaAjaxForm();
    }

    $(document).ready(ideiaFormOnReady);


})(jQuery);