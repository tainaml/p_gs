from apps.community.models import Community
from apps.core.business.content_types import ContentTypeCached
from apps.core.forms.rating import FormRating
from apps.core.models.rating import Rating
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from apps.core.models.course import Course
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from apps.core.forms.course import CourseListForm
from apps.core.views.rating import Rate
from apps.custom_base.views import FormBasePaginetedListView


class CourseListView(FormBasePaginetedListView):

    success_template_path = 'course/page.html'
    success_ajax_template_path = 'course/items.html'
    fail_validation_template_path = 'course/items.html'
    form = CourseListForm
    itens_per_page = 12

    # @Override
    def after_process(self, request=None, *args, **kwargs):
        super(CourseListView, self).after_process(*args, **kwargs)
        self.context.update({'courses': self.process_return, 'form': self.form})


class CourseShowView(View):

    template_path = "course/single.html"
    form = FormRating


    def get_context(self, request, course):

        content_type = ContentTypeCached.objects.get(model="course")
        content_data = {"object_id": course.id, "content_type": content_type}



        try:
            if not request.user.is_authenticated():
                raise Rating.DoesNotExist()
            instance = course.ratings.get(author=request.user)

            form = self.form(instance=instance)

        except Rating.DoesNotExist:

            form = self.form()

        return {
            'instance': course,
            'form': form,
            'content_data': content_data
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


class CourseRate(Rate):
    template_name = 'course/single.html'


class CourseRateDelete(View):

    def get(self, request, rate_id):

        try:
            rate = Rating.objects.get(id=rate_id, author__id=request.user.id)
        except Rating.DoesNotExist, Rating.MultipleObjectsReturned:
            raise Http404(_('Rating does not exist'))

        next_url = request.GET.get('next_url')


        if not next_url:
            next_url = reverse('course:show', args=[rate.content_object.slug])

        # deletes
        rate.delete()

        if request.is_ajax():
            return JsonResponse({
                'next_url': next_url
            })
        else:
            return redirect(to=next_url)

