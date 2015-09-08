from django.contrib import admin
from .models import ObjectTaxonomy, Taxonomy, Term
# Register your models here.

admin.site.register(ObjectTaxonomy)
admin.site.register(Taxonomy)
admin.site.register(Term)