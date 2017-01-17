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


class CurriculumInline(StackedInline):

    form = CurruculumAdminInlineForm

    model = Curriculum
    extra = 0
    min_num = 1




class RatingsInline(GenericStackedInline):

    model = Rating
    extra = 1
    raw_id_fields = ['author']

class ModelFormAdminCourse(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ('rating',)
        widgets = {
            'observation': SummernoteWidget(editor_conf='article_admin')
        }


class CoreCourseAdmin(admin.ModelAdmin):

    list_display = ('title', 'rating', 'internal_author', 'updatein')
    list_display_links = list_display

    inlines = [CurriculumInline, RatingsInline]
    form = ModelFormAdminCourse
    def view_on_site(self, obj):

        return reverse('course:show', args=[obj.slug])

    class Meta:
        widgets = {
            'observation': SummernoteWidget(editor_conf='article_admin')
        }


admin.site.register(Course, CoreCourseAdmin)
admin.site.register(Plataform)