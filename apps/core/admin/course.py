from django.contrib import admin
from apps.core.models.course import Course


class CoreCourseAdmin(admin.ModelAdmin):

    list_display = ('title', 'rating', 'internal_author', 'updatein')
    list_display_links = list_display


admin.site.register(Course, CoreCourseAdmin)