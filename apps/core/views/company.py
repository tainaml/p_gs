from django.shortcuts import render
from django.views import View
from apps.core.models.company import CompanyProxy
from apps.core.forms.company import CompanyForm


class CompanyEditView(View):

    template_path = 'organization/register.html'
    form_class = CompanyForm
    form = None

    def get_context(self, request, company=None):

        return {
            'form': self.form,
            'company': company
        }

    def get(self, request, company_id=None):

        company = None
        try:
            company = CompanyProxy.objects.get(id=company_id)
        except CompanyProxy.DoesNotExist, CompanyProxy.MultipleObjectsReturned:
            pass

        self.form = self.form_class(
            instance=company
        )

        context = self.get_context(request, company)

        return render(
            request,
            template_name=self.template_path,
            context=context
        )



