from django.contrib import admin
from django.db import models
from django import forms
from apps.account.models import User
from apps.company.models import Company, CompanyContact
from django.template.defaultfilters import slugify


class CompanyProxyManager(models.Manager):

    def get_queryset(self):
        qs = super(CompanyProxyManager, self).get_queryset()
        return qs.filter(
            user__usertype=User.ORGANIZATION
        )


class CompanyProxy(Company):

    class Meta:
        proxy = True

    objects = CompanyProxyManager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if not self.user:

            company_user = User.objects.create_user(
                username=slugify(self.name),
                first_name=self.name,
                last_name='',
                is_active=True,
                usertype=User.ORGANIZATION
            )

            company_user.save()

            self.user = company_user
            

        super(CompanyProxy, self).save(force_insert, force_update, using, update_fields)
        #after save


class MembersInline(admin.StackedInline):

    model = CompanyProxy.members.through
    extra = 0


class CompanyContactInline(admin.TabularInline):

    model = CompanyContact
    extra = 1


class CompanyAdmin(admin.ModelAdmin):

    readonly_fields = ['user']
    inlines = [MembersInline, CompanyContactInline]


admin.site.register(CompanyProxy, CompanyAdmin)