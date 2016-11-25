import urllib
from django.shortcuts import render
from django.views import View
from apps.core.forms.course import CourseListForm
from apps.custom_base.views import FormBasePaginetedListView


class CourseListView(FormBasePaginetedListView):
    success_template_path = 'course/page.html'
    form = CourseListForm
    itens_per_page = 6

    # @Override
    def after_process(self, request=None, *args, **kwargs):
        super(CourseListView, self).after_process(*args, **kwargs)
        self.context.update({'courses': self.process_return})


class CourseShowView(View):

    template_path = "#TODO"



    def return_success(self, request, context=None):
        pass

    def get_context(self):

        pass

    def get(self, request):

        pass

