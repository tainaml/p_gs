from apps.userprofile.models import Responsibility, UserProfile
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.views import View
from apps.taxonomy.service import business as TaxonomyBusiness
from ..forms.certification import CertificationFiltersForm
from apps.core.business import user as UserCoreBusiness


class CertificationListView(View):

    template_path = 'certification/list.html'
    template_items = 'certification/items.html'

    form = CertificationFiltersForm

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

class CertificationView(View):

    template_path = 'certification/certification.html'

    def get_context(self, request):

        categories = TaxonomyBusiness.get_categories()

        return {
            'categories': categories,
        }

    def get(self, request, slug):

        try:
            responsibility = Responsibility.objects.get(slug=slug, active=True)
        except Responsibility.DoesNotExist as e:
            raise Http404(_('Certification not found'))

        _context = self.get_context(request)

        # Categories names from this responsibility
        main_categories = responsibility.categories.all()
        categories_names = []

        for category in main_categories:
            categories_names.append(category.description)

        # Peoples with this responsibility
        profiles = UserCoreBusiness.get_active_users().filter(
            occupation__responsibility=responsibility,
        ).order_by('-user__date_joined')

        _context.update({
            'responsibility': responsibility,
            'responsibility_categories': categories_names,
            'profiles_with_this_responsibility': profiles[:9] if profiles else []
        })

        return render(
            request,
            template_name=self.template_path,
            context=_context
        )
