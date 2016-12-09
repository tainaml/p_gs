from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from apps.core.forms.rating import FormRating



class CourseRating(View):

    form = FormRating

    @method_decorator(login_required)
    def get(self, request):


        data = {'author': request.user.id}
        data.update(request.GET.dict())

        form = self.form(data=data)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'value': form.cleaned_data['value']}, status=200)
        else:
            return JsonResponse(data={'errors': form.errors}, status=400)






