from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from apps.core.forms.rating import FormRating
from apps.core.models.rating import Rating


class TemplateNotDefinedException(Exception):
    pass


class Rate(View):

    form = FormRating

    context = {}

    def get_context(self):
        return {}

    @property
    def template_name(self):
        raise TemplateNotDefinedException()

    @method_decorator(login_required)
    def post(self, request):

        data = {'author': request.user.id}
        data.update(request.POST.dict())
        try:
            rating = Rating.objects.get(
                content_type=request.POST['content_type'],
                object_id=request.POST['object_id'],
                author=request.user
            )
            form = self.form(instance=rating, data=data)
        except Rating.DoesNotExist, ValueError:

            form = self.form(data=data)

        self.context.update({
            'form': form
        })

        if form.is_valid():
            form.save()
            self.context.update({'instance': form.instance.content_object})

        self.context.update(self.get_context())

        return render(request=request, template_name=self.template_name, context=self.context)









