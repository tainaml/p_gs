from django.views import View
from apps.core.models.company import


class CompanyEditView(View):

    def get_context(self, request, company=None):

        return {

        }


    def get(self, request, company_id=None):

        company = None

        context = self.get_context(request, )



