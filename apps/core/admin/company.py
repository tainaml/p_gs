from django.contrib import admin
from django.db import models
from apps.account.models import User
from apps.account.admin import UserNewAdmin
from apps.company.models import Company, CompanyContact, Membership
from jet.admin import CompactInline


class CompanyProxyManager(models.Manager):

    def get_queryset(self):
        qs = super(CompanyProxyManager, self).get_queryset()
        return qs.filter(
            user__usertype=User.ORGANIZATION
        )


class CompanyProxy(Company):

    objects = CompanyProxyManager()

    class Meta:

        proxy = True


class MembersInline(admin.StackedInline):

    model = CompanyProxy.members.through
    extra = 0


class CompanyContactInline(admin.TabularInline):

    model = CompanyContact
    extra = 1



class CompanyAdmin(admin.ModelAdmin):

    inlines = [MembersInline, CompanyContactInline]


admin.site.register(CompanyProxy, CompanyAdmin)