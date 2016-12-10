from apps.community.models import Community
from apps.core.business.content_types import ContentTypeCached
from apps.core.forms.rating import FormRating
from apps.core.models.rating import Rating
from django.utils.translation import ugettext_lazy as _
from apps.core.models.course import Course
from django.http import Http404
from django.shortcuts import render
from django.views import View
from apps.core.forms.course import CourseListForm
from apps.custom_base.views import FormBasePaginetedListView


class CourseListView(FormBasePaginetedListView):

    success_template_path = 'course/page.html'
    success_ajax_template_path = 'course/items.html'
    fail_validation_template_path = 'course/page.html'
    form = CourseListForm
    itens_per_page = 6

    # @Override
    def after_process(self, request=None, *args, **kwargs):
        super(CourseListView, self).after_process(*args, **kwargs)
        self.context.update({'courses': self.process_return, 'form': self.form})


class CourseShowView(View):

    template_path = "course/single.html"
    form = FormRating


    def get_context(self, request, course):

        try:
            instance = course.ratings.get(author=request.user)
            form = self.form(instance=instance)

        except Rating.DoesNotExist:
            content_type = ContentTypeCached.objects.get(model="course")
            form_data = {"object_id": course.id, "content_type": content_type}

            form = self.form(data=form_data, instance=None)
        return {
            'course': course,
            'form': form
        }

    def get(self, request, course_slug):

        try:
            course = Course.objects.prefetch_related("ratings", "curriculums", "related_courses").get(slug=course_slug)
        except Course.DoesNotExist:
            raise Http404(_('Course not found'))

        context = self.get_context(request, course)

        return render(
            request,
            template_name=self.template_path,
            context=context
        )

