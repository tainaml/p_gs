from django import forms
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.forms import inlineformset_factory
from ideia_summernote.widget import SummernoteWidget
from apps.core.models.course import Course, Curriculum



class CurriculumInline(StackedInline):

    model = Curriculum
    extra = 0
    min_num = 1


class CoreCourseAdmin(admin.ModelAdmin):

    list_display = ('title', 'rating', 'internal_author', 'updatein')
    list_display_links = list_display


    inlines = [CurriculumInline]

admin.site.register(Course, CoreCourseAdmin)