from django.contrib import admin

from .models import Taxonomy, Term

# Register your models here.

admin.site.register(Taxonomy)
admin.site.register(Term)