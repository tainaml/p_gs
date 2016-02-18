from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View


# Create your views here.


class FormBaseView(View):
    context = {}
    process_return = None

    @property
    def form(self):
        raise NotImplementedError("you must specify the form")

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

    def __response_ajax__(self, request, *args, **kwargs):
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

    def __response_postback__(self, request, *args, **kwargs):
        return render(request,
                      self.success_template_path if self.form.is_valid() else
                      self.fail_validation_template_path,
                      self.context,
                      *args,
                      **kwargs)

    def do_process(self, request=None, *args, **kwargs):

        self.before_process(request, *args, **kwargs)
        self.process_return = self.form.process()
        self.after_process(request, *args, **kwargs)
        self.context.update({'form': self.form})

        if request.is_ajax:
            return self.__response_ajax__(request, *args, **kwargs)
        else:
            return self.__response_postback__(request, *args, **kwargs)

class InstanceSaveFormBaseView(FormBaseView):
    form = None

    # @Override
    def after_process(self, request=None, *args, **kwargs):
        self.context.update({'instance': self.process_return})

    @method_decorator(login_required)
    def post(self, request=None, *args, **kwargs):
        if not self.form:
            raise NotImplementedError("You must specify the form")
        self.form = self.form(request.user, request.POST)

        return super(InstanceSaveFormBaseView, self).do_process(request)


class InstanceUpdateFormBaseView(InstanceSaveFormBaseView):
    form = None

    def instance_to_update(self, request, *args, **kwargs):
        raise NotImplementedError("you must specify how to get the instance to update")


    @method_decorator(login_required)
    def post(self, request=None, *args, **kwargs):
        instance_to_update = self.instance_to_update(request, *args, **kwargs)

        if not instance_to_update:
            raise Http404()
        if not self.form:
            raise NotImplementedError("You must specify the form")

        self.form = self.form(request.user, instance_to_update,
                                      request.POST)

        return super(InstanceUpdateFormBaseView, self).do_process(request)