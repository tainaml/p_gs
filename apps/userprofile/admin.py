from apps.taxonomy.models import Taxonomy
from django.contrib import admin
from django import forms
from apps.userprofile.models import Responsibility, UserProfile
from ideia_summernote.widget import SummernoteWidget


class ResponsibilityAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResponsibilityAdminForm, self).__init__(*args, **kwargs)
        self.fields['categories'].queryset = Taxonomy.objects.filter(term__slug='categoria')


    class Media:
        js = (
            # 'https://code.jquery.com/jquery-2.2.4.min.js',
            'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.1/summernote.min.js', )

        css= {
            'all': (
                'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
                'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.1/summernote.css',
            )
        }

    class Meta:
        exclude = ()
        widgets = {
            'about': SummernoteWidget(editor_conf='article'),
            'study': SummernoteWidget(editor_conf='article'),
            'main_activity': SummernoteWidget(editor_conf='article'),
            'more_info': SummernoteWidget(editor_conf='article'),
        }

class ResponsibilityAdmin(admin.ModelAdmin):

    form = ResponsibilityAdminForm

    filter_horizontal  = ('categories',)

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'categories')
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


admin.site.register(Responsibility, ResponsibilityAdmin)
admin.site.register(UserProfile)