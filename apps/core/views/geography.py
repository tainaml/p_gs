from django.http import JsonResponse, Http404
from django.views import View
from apps.core.exceptions.geography import NotSearchableModelException
from apps.core.forms.geography import GeographyListForm
from django.core import serializers

class Search(View):

    form = GeographyListForm
    itens_per_page = 10

    def get(self, request, model):

        self.form = self.form(data=request.GET, itens_per_page=self.itens_per_page, model=model)
        try:
            locales = self.form.process()

            data = serializers.serialize('json', locales)
            return JsonResponse(data=data, safe=False)
        except NotSearchableModelException:
            raise Http404()


