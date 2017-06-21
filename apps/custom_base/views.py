from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

# Create your views here.

class FormBaseView(View):
    context = {}
    process_return = None
    form = None

    @property
    def success_template_path(self):
        raise NotImplementedError("you must specify the success_template_path")

    @property
    def fail_validation_template_path(self):
        raise NotImplementedError(
            "you must specify the fail_validation_template_path")

    def before_process(self, request=None, *args, **kwargs):
        pass

    def after_process(self, request=None, *args, **kwargs):
        pass

    def __response_json__(self, request, *args, **kwargs):
        response_data = {}
        is_valid = self.form.is_valid()
        if is_valid:
            response_data['is_valid'] = is_valid
            response_data['template'] = render(request,
                                               self.success_template_path,
                                               self.context).content
        else:
            response_data['errors'] = self.form.errors

        return JsonResponse(response_data,
                            status=200 if is_valid else 400, *args,
                            **kwargs)

    def __response_render__(self, request, *args, **kwargs):
        return render(request,
                      self.success_template_path if self.form.is_valid() else
                      self.fail_validation_template_path,
                      self.context,
                      *args,
                      **kwargs)

    def fill_form_kwargs(self, request=None, *args, **kwargs):
        return {'data': request.GET}

    def do_process(self, request=None, *args, **kwargs):
        if not self.form:
            raise NotImplementedError("you must specify the class form. Ex: form = FooForm")
        self.before_process(request, *args, **kwargs)
        form_kwarg = self.fill_form_kwargs(request)
        self.form = self.form(**form_kwarg)
        self.process_return = self.form.process()
        self.after_process(request, *args, **kwargs)
        self.context.update({'form': self.form})

        if request.is_ajax:
            return self.__response_json__(request, *args, **kwargs)
        else:
            return self.__response_render__(request, *args, **kwargs)


class FormBaseListView(FormBaseView):
    form = None
    itens_per_page = 10

    # @Override
    def fill_form_kwargs(self, request=None, *args, **kwargs):
        return {'data': request.GET, 'itens_per_page': self.itens_per_page}

    # @Override
    def after_process(self, request=None, *args, **kwargs):
        self.context.update({'instance_list': self.process_return})
        self.context.update({'form': self.form})
        cleaned_data = self.form.cleaned_data if hasattr(self.form, "cleaned_data") else {'page': 1}
        cleaned_data['page']+=1
        self.context.update(cleaned_data)

    # @Override
    def do_process(self, request=None, *args, **kwargs):
        if not self.form:
            raise NotImplementedError("you must specify the class form. Ex: form = FooForm")
        self.before_process(request, *args, **kwargs)
        self.form = self.form(**self.fill_form_kwargs(request))
        self.process_return = self.form.process()
        self.after_process(request, *args, **kwargs)
        if request.GET.get("page"):
            return self.__response_render__(request, *args, **kwargs)
        else:
            return self.__response_json__(request, *args, **kwargs)

    def get(self, request=None, *args, **kwargs):
        if not self.form:
            raise NotImplementedError("You must specify the form")


        return self.do_process(request, *args, **kwargs)


class FormBasePaginetedListView(FormBaseListView):
    form = None
    itens_per_page = 10

    @property
    def success_ajax_template_path(self):
        raise NotImplementedError("you must specify the success_ajax_template_path")


    # @Override
    def after_process(self, request=None, *args, **kwargs):
        self.context.update({'instance_list': self.process_return})
        self.context.update({'form': self.form})
        cleaned_data = self.form.cleaned_data if hasattr(self.form, "cleaned_data") else {'page': 1}
        cleaned_data['page']+=1
        self.context.update(cleaned_data)

    def after_fill(self, request, *args, **kwargs):
        pass

    # @Override
    def do_process(self, request=None, *args, **kwargs):
        if not self.form:
            raise NotImplementedError("you must specify the class form. Ex: form = FooForm")
        self.before_process(request, *args, **kwargs)
        self.form = self.form(**self.fill_form_kwargs(request))
        self.after_fill(request, *args, **kwargs)
        self.process_return = self.form.process()
        self.after_process(request, *args, **kwargs)

        return self.__response_render__(request, *args, **kwargs)

    def __response_render__(self, request, *args, **kwargs):
        return render(request,
                      (self.success_ajax_template_path if request.is_ajax()
                       else  self.success_template_path)if self.form.is_valid() else
                      self.fail_validation_template_path,
                      self.context,
                      *args,
                      **kwargs)


class InstanceSaveFormBaseView(FormBaseView):
    form = None

    # @Override
    def after_process(self, request=None, *args, **kwargs):
        self.context.update({'instance': self.process_return})

    # @Override
    def fill_form_kwargs(self, request=None, *args, **kwargs):
        return {'user': request.user, 'data': request.POST}

    @method_decorator(login_required)
    def post(self, request=None, *args, **kwargs):
        if not self.form:
            raise NotImplementedError("You must specify the form")

        return super(InstanceSaveFormBaseView, self).do_process(request)


class InstanceUpdateFormBaseView(InstanceSaveFormBaseView):
    form = None

    def instance_to_update(self, request, *args, **kwargs):
        raise NotImplementedError("you must specify how to get the instance to update")

    # @Override
    def fill_form_kwargs(self, request=None, *args, **kwargs):
        return {'user': request.user, 'instance': self.instance_to_update(request, *args, **kwargs),
                'data': request.POST}

    @method_decorator(login_required)
    def post(self, request=None, *args, **kwargs):
        instance = self.instance_to_update(request, *args, **kwargs)

        if not instance:
            raise Http404()
        if not self.form:
            raise NotImplementedError("You must specify the form")

        return super(InstanceUpdateFormBaseView, self).do_process(request)


class InstanceDeleteFormBaseView(FormBaseView):

    def __response_json__(self, request, *args, **kwargs):
        response_data = {}
        is_valid = self.form.is_valid()
        if is_valid:
            response_data['status'] = self.process_return
        else:
            response_data['errors'] = self.form.errors

        return JsonResponse(response_data,
                            status=200 if is_valid else 400, *args,
                            **kwargs)

