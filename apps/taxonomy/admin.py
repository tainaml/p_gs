from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Taxonomy, Term


class TaxonomyInLine(admin.TabularInline):
    model = Taxonomy


class TaxonomyAdmin(VersionAdmin):
    list_display = ('description', 'slug','parent','term',)
    list_filter = ('term', 'parent',)
    search_fields = ['description', 'slug']
    inlines = [
        TaxonomyInLine,
    ]


admin.site.register(Taxonomy, TaxonomyAdmin)
admin.site.register(Term)
