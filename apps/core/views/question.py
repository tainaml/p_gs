from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _

from apps.community.models import Community
from apps.question import views
from ..forms import question as QuestionForms
from ..business import question as BusinessQuestion
from ..business import feed as BusinessFeed
from apps.core.business import user as UserBusiness



class CoreQuestionCreateView(views.CreateQuestionView):
    form = QuestionForms.CoreCreateQuestionForm

    def prepare_context(self, request, context):
        context = super(CoreQuestionCreateView, self).prepare_context(request, context)
        communities = UserBusiness.get_user_communities_list(request.user)

        context.update(communities=communities)
        return context


class CoreSaveQuestionView(views.SaveQuestionView):
    form = QuestionForms.CoreCreateQuestionForm


class CoreEditQuestionView(views.EditQuestionView):
    form = QuestionForms.CoreEditQuestionForm

    def prepare_context(self, request, context):
        context = super(CoreEditQuestionView, self).prepare_context(request, context)
        communities = UserBusiness.get_user_communities_list(request.user)

        context.update(communities=communities)
        return context


class CoreUpdateQuestionView(views.UpdateQuestionView):
    form = QuestionForms.CoreEditQuestionForm


class CoreQuestionInCommunityView(CoreQuestionCreateView):

    question_community = False

    @method_decorator(login_required)
    def get(self, request, community_slug=None, *args, **kwargs):

        try:
            self.question_community = Community.objects.get(slug=community_slug)
        except Community.DoesNotExist, e:
            raise Http404(_('Community not Found'))

        # raize 403 if user not follow this community
        if self.question_community:
            user_communities = UserBusiness.get_user_communities(request.user)
            if self.question_community not in user_communities:
                raise PermissionDenied(_('User need follow this community'))

        return super(CoreQuestionInCommunityView, self).get(request, *args, **kwargs)

    def prepare_initial_data(self, initial):
        initial.update(communities=[self.question_community])
        return initial

    def prepare_context(self, request, context):

        context = super(CoreQuestionInCommunityView, self).prepare_context(request, context)

        form = context.get('form', None)

        if form and 'communities' in form.fields:
            form.fields["communities"].initial = self.question_community
            context.update(form_article=form)

        return context


class CoreQuestionRelatedView(views.View):

    template_path = "question/partials/question-related-questions-list.html"

    def return_success(self, request, context=None):

        if request.is_ajax():

            return JsonResponse({
                'template': render(request, self.template_path, context).content
            }, status=200)


    def get(self, request, question_id, content_type):

        related_list = BusinessQuestion.get_related(question_id, content_type, 4, 1)

        context = {'questions': related_list}

        return self.return_success(request, context)


class CoreQuestionView(views.ShowQuestionView):

    def get_context(self, request, question_instance=None):
        feed_object = BusinessFeed.BusinessFeed.get_feed(question_instance)
        return {
            'feed': feed_object
        }