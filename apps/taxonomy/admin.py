from django.contrib import admin

from .models import Taxonomy, Term

class TaxonomyInLine(admin.TabularInline):
    model = Taxonomy

class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('description', 'slug','parent','term',)
    list_filter = ('term', 'parent',)

    inlines = [
        TaxonomyInLine,
    ]
# Register your models here.

admin.site.register(Taxonomy, TaxonomyAdmin)
admin.site.register(Term)