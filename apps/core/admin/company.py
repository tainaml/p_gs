from apps.userprofile.models import UserProfile
from django.conf import settings
from django.contrib import admin
from django.db import models
from django import forms
from apps.account.models import User
from apps.company.models import Company, CompanyContact, CompanyManager, Membership
from django.template.defaultfilters import slugify
from jet.admin import CompactInline
from apps.core.models.company import CompanyProxy


class MembersInline(CompactInline):

    model = CompanyProxy.members.through
    extra = 1
    raw_id_fields = ['user']


class CompanyContactInline(admin.TabularInline):

    model = CompanyContact
    extra = 1


class CompanyAdmin(admin.ModelAdmin):

    readonly_fields = ['user']
    inlines = [MembersInline, CompanyContactInline]

    def get_queryset(self, request):
        return self.model.organizations.all()


admin.site.register(CompanyProxy, CompanyAdmin)