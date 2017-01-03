from django.contrib import admin

# Register your models here.

from apps.company.models import CompanyContact, Company, CompanyContactType


class ContactInLine(admin.TabularInline):
    model = CompanyContact

class CompanyAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', 'city']

    inlines = [
            ContactInLine,
        ]



admin.site.register(CompanyContactType)
admin.site.register(Company, CompanyAdmin)