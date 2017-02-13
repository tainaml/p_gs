from django import forms
from django.contrib import admin

# Register your models here.
from ideia_summernote.widget import SummernoteWidget
from apps.certification.models import Certification
from apps.taxonomy.models import Taxonomy


class CertificationAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CertificationAdminForm, self).__init__(*args, **kwargs)
        self.fields['taxonomies'].queryset = Taxonomy.objects.filter(term__slug='comunidade')

    class Meta:
        exclude = ()
        widgets = {
            'description': SummernoteWidget(editor_conf='responsibility'),
            'about': SummernoteWidget(editor_conf='responsibility'),
            'where_get': SummernoteWidget(editor_conf='responsibility'),
            'more_info': SummernoteWidget(editor_conf='responsibility'),
        }

class CertificationAdmin(admin.ModelAdmin):

    form = CertificationAdminForm

    filter_horizontal = ('taxonomies',)


admin.site.register(Certification, CertificationAdmin)