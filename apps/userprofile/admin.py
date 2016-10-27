from django.contrib import admin
from django import forms
from apps.userprofile.models import Responsibility, UserProfile
from ideia_summernote.widget import SummernoteWidget


class ResponsibilityAdminForm(forms.ModelForm):

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
            'text': SummernoteWidget(editor_conf='community')
        }

class ResponsibilityAdmin(admin.ModelAdmin):

    form = ResponsibilityAdminForm


admin.site.register(Responsibility, ResponsibilityAdmin)
admin.site.register(UserProfile)