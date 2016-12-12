from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from apps.core.business.content_types import ContentTypeCached
from apps.core.forms.rating import FormRating
from apps.core.models.rating import Rating
from django.contrib.contenttypes.models import ContentType

class TemplateNotDefinedException(Exception):
    pass


class Rate(View):

    form = FormRating

    context = {}
    content_object = None

    def get_context(self):
        return {}

    @property
    def template_name(self):
        raise TemplateNotDefinedException()

    @method_decorator(login_required)
    def post(self, request):

        data = {'author': request.user.id}
        data.update(request.POST.dict())
        content_object = self.__get_content_object__(request.POST['content_type'], request.POST['object_id'])
        content_type = ContentType.objects.get_for_model(model=content_object)

        try:
            rating = Rating.objects.get(
                content_type=content_type,
                object_id=content_object.id,
                author=request.user
            )
            form = self.form(instance=rating, data=data)
        except Rating.DoesNotExist:

            form = self.form(data=data)

        self.context.update({
            'form': form,
            'content_data': {
                'object_id': content_object.id,
                'content_type': content_type
            }
        })



        if form.is_valid():
            form.save()
            self.context.update({'instance': form.instance.content_object})


        self.context.update(self.get_context())

        return render(request=request, template_name=self.template_name, context=self.context)

    def __get_content_object__(self, content_type, object_id):

        try:
            content_type = ContentType.objects.get(id=content_type)
            content_object = content_type.get_object_for_this_type(id=object_id)
            return content_object
        except ValueError, ContentType.DoesNotExist:
            raise Http404()










