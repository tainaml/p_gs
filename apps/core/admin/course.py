from django.urls import reverse
from apps.core.models.rating import Rating
from django import forms
from django.contrib import admin
from django.contrib.admin import StackedInline
from ideia_summernote.widget import SummernoteWidget
from apps.core.models.course import Course, Curriculum
from apps.core.models.plataform import Plataform
from django.contrib.contenttypes.admin import GenericStackedInline

class CurruculumAdminInlineForm(forms.ModelForm):


    class Meta:
        model = Curriculum
        exclude = ()
        widgets = {
            'description': SummernoteWidget(editor_conf='article_admin')
        }

    class Media:
        js = (
            'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.1/summernote.min.js', )

        css= {
            'all': (
                'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
                'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.1/summernote.css',
            )
        }

class CurriculumInline(StackedInline):

    form = CurruculumAdminInlineForm

    model = Curriculum
    extra = 0
    min_num = 1



class RatingsInline(GenericStackedInline):

    model = Rating
    extra = 1
    raw_id_fields = ['author']




class CoreCourseAdmin(admin.ModelAdmin):

    list_display = ('title', 'rating', 'internal_author', 'updatein')
    list_display_links = list_display

    inlines = [CurriculumInline, RatingsInline]

    def view_on_site(self, obj):

        return reverse('course:show', args=[obj.slug])



admin.site.register(Course, CoreCourseAdmin)
admin.site.register(Plataform)