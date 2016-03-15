from django.contrib import admin

from .models import Taxonomy, Term

class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('description', 'slug', 'term',)
    list_filter = ('term',)

# Register your models here.

admin.site.register(Taxonomy, TaxonomyAdmin)
admin.site.register(Term)