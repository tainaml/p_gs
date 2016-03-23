from django.contrib import admin
from reversion_compare.admin import CompareVersionAdmin

from .models import Taxonomy, Term


class TaxonomyInLine(admin.TabularInline):
    model = Taxonomy


class TaxonomyAdmin(CompareVersionAdmin):
    list_display = ('description', 'slug','parent','term',)
    list_filter = ('term', 'parent',)

    inlines = [
        TaxonomyInLine,
    ]


admin.site.register(Taxonomy, TaxonomyAdmin)
admin.site.register(Term)
