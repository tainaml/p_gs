from django.http import Http404
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View
from apps.taxonomy.service import business as TaxonomyBusiness
from ..forms.responsibility import ResponsibilityFiltersForm


class ResponsibilityView(View):

    template_path = 'responsibilities/list.html'
    template_items = 'responsibilities/items.html'

    form = ResponsibilityFiltersForm

    def get_context(self, request):

        categories = TaxonomyBusiness.get_categories()

        form = self.form(
            data=request.GET,
        )

        responsibilities = form.process()

        return {
            'categories': categories,
            'responsibilities': responsibilities,
        }

    def get(self, request):

        context = self.get_context(request)

        if request.is_ajax():

            _context = {
                'category': request.GET.get('category'),
                'criteria': request.GET.get('criteria'),
                'page': request.GET.get('page', 1),
                'template': render(request, self.template_items, context).content
            }
            return render(request, self.template_items, context)

        return render(
            request,
            template_name=self.template_path,
            context=context
        )