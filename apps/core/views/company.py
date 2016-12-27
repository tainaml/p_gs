from apps.community.models import Community
from apps.core.business.user import get_user_communities_list_from_queryset
from django import forms
from django.forms import widgets
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from apps.core.models.company import CompanyProxy
from apps.company.models import Membership
from apps.core.forms.company import CompanyForm
from django.shortcuts import redirect


class CompanyEditView(View):

    template_path = 'organization/register.html'
    form_class = CompanyForm
    form = None

    def get_company(self, company_id):
        company = None
        try:
            company = CompanyProxy.objects.get(id=company_id)
        except CompanyProxy.DoesNotExist, CompanyProxy.MultipleObjectsReturned:
            pass

        return company

    def get_context(self, request, company=None):

        communities = Community.objects.exclude(
            taxonomy__term__slug='categoria'
        )

        communities_list = get_user_communities_list_from_queryset(communities, author=None, id_field='taxonomy_id')

        members_formset = forms.inlineformset_factory(
            parent_model=CompanyProxy,
            model=CompanyProxy.members.through,
            exclude=(),
            can_delete=True,
            widgets={
                'user': widgets.HiddenInput,
                'permission': widgets.HiddenInput
            },
            extra=1,
        )

        members_formset = members_formset(data=request.POST if request.POST else None, instance=company)

        return {
            'form': self.form,
            'company': company,
            'members_formset': members_formset,
            'communities': communities_list
        }

    def get(self, request, company_id=None):

        company = self.get_company(company_id)

        self.form = self.form_class(
            instance=company
        )

        context = self.get_context(request, company)

        return render(
            request,
            template_name=self.template_path,
            context=context
        )

    def post(self, request, company_id=None):

        company = self.get_company(company_id)

        self.form = self.form_class(
            instance=company,
            data=request.POST,
            files=request.FILES,
        )

        context = self.get_context(request, company)

        if self.form.is_valid():
            self.form.save()

            return redirect(
                reverse('organization:edit', args=[self.form.instance.id])
            )

        return render(
            request,
            template_name=self.template_path,
            context=context
        )


