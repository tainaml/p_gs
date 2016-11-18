from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.forms import FlatpageForm
from ideia_summernote.widget import SummernoteWidget


class CoreFlatPageForm(FlatpageForm):

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

        widgets = {
            'content': SummernoteWidget(editor_conf='article_admin')
        }


class CoreFlatPageAdmin(FlatPageAdmin):

    form = CoreFlatPageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CoreFlatPageAdmin)