from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.forms import FlatpageForm
from ideia_summernote.widget import SummernoteWidget


class CoreFlatPageForm(FlatpageForm):


    class Meta:

        widgets = {
            'content': SummernoteWidget(editor_conf='article_admin')
        }


class CoreFlatPageAdmin(FlatPageAdmin):

    form = CoreFlatPageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CoreFlatPageAdmin)