from apps.community.models import Community
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

    def get_context(self, request, course):

        taxs = course.taxonomies.all()
        communities = Community.objects.filter(taxonomy__in=taxs)

        avaliations = course.ratings.all()
        user_avaliation = None

        try:
            user_avaliation = avaliations.get(author=request.user)
        except Rating.DoesNotExist, Rating.MultipleObjectsReturned:
            pass
        except Exception as e:
            print(e)

        return {
            'course': course,
            'curriculums': course.curriculums.all(),
            'course_communities': communities,
            'user_avaliation': user_avaliation,
            'related_courses': course.related_courses.all(),
            'course_avaliations': avaliations.exclude(author=request.user),
        }

    def get(self, request, course_slug):

        try:
            course = Course.objects.get(slug=course_slug)
        except Course.DoesNotExist:
            raise Http404(_('Course not found'))

        context = self.get_context(request, course)

        return render(
            request,
            template_name=self.template_path,
            context=context
        )

