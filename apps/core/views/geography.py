from django.forms import model_to_dict
from django.http import JsonResponse, Http404
from django.views import View
from apps.core.exceptions.geography import NotSearchableModelException
from apps.core.forms.geography import GeographyListForm

class Search(View):

    form = GeographyListForm
    itens_per_page = 10

    def get(self, request, model):

        self.form = self.form(data=request.GET, itens_per_page=self.itens_per_page, model=model)
        try:
            locales = self.form.process()

            return JsonResponse(data=[model_to_dict(locale) for locale in locales], safe=False)
        except NotSearchableModelException:
            raise Http404()


