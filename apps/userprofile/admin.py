from apps.taxonomy.models import Taxonomy
from django.contrib import admin
from django import forms
from apps.userprofile.models import Responsibility, UserProfile
from ideia_summernote.widget import SummernoteWidget


class ResponsibilityAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResponsibilityAdminForm, self).__init__(*args, **kwargs)
        self.fields['categories'].queryset = Taxonomy.objects.filter(term__slug='categoria')

    class Meta:
        exclude = ()
        widgets = {
            'about': SummernoteWidget(editor_conf='responsibility', load_init=False),
            'study': SummernoteWidget(editor_conf='responsibility', load_init=False),
            'main_activity': SummernoteWidget(editor_conf='responsibility', load_init=False),
            'more_info': SummernoteWidget(editor_conf='responsibility', load_init=False),
        }

class ResponsibilityAdmin(admin.ModelAdmin):

    form = ResponsibilityAdminForm

    filter_horizontal  = ('categories',)

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'active', 'categories')
        }),

        ('About', {
            'fields': ('about',)
        }),

        ('Study', {
            'fields': ('study',)
        }),

        ('Main Activity', {
            'fields': ('main_activity',)
        }),

        ('More Info', {
            'fields': ('more_info',)
        }),
    )


class UserProfileAdmin(admin.ModelAdmin):

    raw_id_fields = ['user', 'city', 'city_hometown']


admin.site.register(Responsibility, ResponsibilityAdmin)
admin.site.register(UserProfile, UserProfileAdmin)