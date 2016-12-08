from apps.userprofile.models import UserProfile
from django.contrib import admin
from django.db import models
from django import forms
from apps.account.models import User
from apps.company.models import Company, CompanyContact
from django.template.defaultfilters import slugify
from jet.admin import CompactInline


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

    def create_user(self):

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

            user_profile = self.user.user_profile
            user_profile.profile_picture = self.logo
            user_profile.description = self.description
            user_profile.save()

        return self.user

    def update_user(self):

        if not self.user:
            return None

        self.user.first_name = self.name
        self.user.save()

        try:

            user_profile = UserProfile.objects.get(user=self.user)
            user_profile.profile_picture = self.logo
            user_profile.description = self.description
            user_profile.save()

        except Exception as e:
            print(e)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.create_user()
        super(CompanyProxy, self).save(force_insert, force_update, using, update_fields)
        self.update_user()


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


admin.site.register(CompanyProxy, CompanyAdmin)