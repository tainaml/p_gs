from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseForbidden
from apps.community.models import Community
from apps.core.business.user import get_user_communities_list_from_queryset
from django import forms
from django.contrib.auth.decorators import login_required
from django.forms import widgets
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from apps.core.models.company import CompanyProxy
from apps.company.models import Membership
from apps.core.forms.company import CompanyForm
from django.shortcuts import redirect


class CompanyEditView(View):

    template_path = 'organization/register.html'
    form_class = CompanyForm
    form = None
    members_formset = None

    def get_company(self, company_id, request_user=None):

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



        return {
            'company': company,
            'communities': communities_list
        }

    @method_decorator(login_required)
    def get(self, request, company_id=None):

        # TODO refactor turning it to a decorator
        if not((request.user.is_company() and request.user.company.id==int(company_id))
               or getattr(request.session, 'before_user_permission', None) == Membership.ADMIN):
            return HttpResponseForbidden()

        company = self.get_company(company_id, request.user)

        self.form = self.form_class(
            instance=company
        )

        members_formset = self.get_members_formset()
        self.members_formset = members_formset(instance=company)

        context = self.get_context(request, company)

        context.update({'form': self.form, 'members_formset': self.members_formset})

        return render(
            request,
            template_name=self.template_path,
            context=context
        )

    @staticmethod
    def get_members_formset():
         return forms.inlineformset_factory(
                    parent_model=CompanyProxy,
                    model=CompanyProxy.members.through,
                    exclude=(),
                    can_delete=True,
                    widgets={
                        'user': widgets.HiddenInput,
                        'permission': widgets.HiddenInput
                    },
                    extra=0,
                )


    @transaction.atomic
    @method_decorator(login_required)
    def post(self, request, company_id=None):

        company = self.get_company(company_id, request.user)

        self.form = self.form_class(
            instance=company,
            data=request.POST,
            files=request.FILES,
        )

        context = self.get_context(request, company)
        members_formset = self.get_members_formset()
        self.members_formset = members_formset(data=request.POST, instance=company)
        context.update({'form': self.form, 'members_formset': self.members_formset})

        #TODO refactor allt this. It was nothing working!
        if self.form.is_valid() and self.members_formset.is_valid():
            self.form.set_request_user(request.user)
            self.form.save(commit=False)

            self.members_formset = members_formset(data=request.POST, instance=self.form.instance)
            self.members_formset.full_clean()
            self.form.instance.save()
            taxonomies = [tax for tax in self.form.cleaned_data.get('categories', [])] + [tax for tax in self.form.cleaned_data.get('communities', [])]
            self.form.instance.taxonomies = taxonomies
            self.form.instance.save()
            self.members_formset.save()


            return redirect(
                reverse('organization:edit', args=[self.form.instance.id])
            )

        return render(
            request,
            template_name=self.template_path,
            context=context
        )
