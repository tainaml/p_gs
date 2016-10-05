# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.community.models import Community
from apps.core.business.content_types import ContentTypeCached
from apps.core.forms.WizardForm import WizardFormStepOne
from apps.core.forms.user import CoreUserProfileForm, CoreUserProfileFullEditForm, CoreSearchFollowers, CoreSearchArticlesForm, CoreSearchVideosForm, \
    CoreSearchCommunitiesForm, CoreRemoveSocialActionForm, CoreSearchSocialActionsForm, CoreUserMyQuestionsForm, \
    CoreSearchQuestionsForm, CoreUserProfileEditStepOne
from apps.core.forms.community import CoreCommunityFormSearch
from apps.core.forms.user import CoreUserSearchForm, CoreUserProfileEditForm
from apps.article.models import Article
from apps.userprofile import views
from apps.userprofile.models import Occupation, Responsibility
from apps.userprofile.service import business as BusinessUserProfile
from apps.taxonomy.service import business as BusinessTaxonomy
from apps.socialactions.service import business as BusinessSocialActions
from apps.core.forms.user import CoreSearchFollowings
from rede_gsti import settings
from apps.community.service import business as BusinessCommunity
from apps.socialactions.service import business as BusinnesSocialAction
class CoreUserView(views.ProfileShowView):

    template_path = 'userprofile/profile.html'
    form = CoreUserSearchForm

    def get_context(self, request, profile_instance=None):
        context = super(CoreUserView, self).get_context(request, profile_instance)
        items_by_page = 5

        form = self.form(
            profile_instance,
            ['article', 'question'],
            items_by_page,
            request.user,
            request.GET
        )

        feed_objects = form.process()

        context.update({
            'feed_objects': feed_objects,
            'form': form,
            'page': form.cleaned_data.get('page', 0) + 1
        })

        return context

    def get(self, request, username=None):
        profile = self.filter(request, request.user)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return render(request, self.template_path, context)


class CoreUserList(CoreUserView):

    template_path = 'userprofile/partials/user-profile-feed.html'

    def get(self, request, username=None):

        profile = self.filter(request, request.user)
        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return render(request, self.template_path, context)


class CoreUserProfile(CoreUserView):
    template_path = 'userprofile/profile-list.html'
    template_path_ajax = 'userprofile/partials/user-profile-list.html'

    form = CoreUserProfileForm

    def get(self, request, username=None):
        profile = self.filter(request, username)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        self.template_path = self.template_path if not request.is_ajax() else self.template_path_ajax

        return render(request, self.template_path, context)

    def get_context(self, request, profile_instance=None):
        content_type = ContentTypeCached.objects.get(model='article')

        itens_by_page = 5

        form = self.form(
            profile_instance,
            content_type.id,
            itens_by_page,
            profile_instance.user,
            request.GET
        )

        feed_objects = form.process()

        return {
            'feed_objects': feed_objects,
            'form': form,
            'page': form.cleaned_data.get('page', 0) + 1
        }



class CoreUserSearch(CoreUserView):

    form = CoreUserProfileForm
    template_path = 'userprofile/profile-search.html'

    def get_context(self, request, profile_instance=None):

        items_per_page = 5
        content_type = ContentTypeCached.objects.get(model='article')

        form = self.form(
            profile_instance,
            content_type.id,
            items_per_page,
            profile_instance.user,
            request.GET
        )

        feed_objects = form.process()

        return {
            'feed_objects': feed_objects,
            'form': form,
            'page': form.cleaned_data.get('page', 0) + 1
        }

    def get(self, request, username=None):
        profile = self.filter(request, username)
        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return render(request, self.template_path, context)


class CoreUserFeed(CoreUserView):
            
    template_path = 'userprofile/profile-feed.html'

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        return super(CoreUserFeed, self).get(request)

    def get_context(self, request, profile_instance=None):
        context = super(CoreUserFeed, self).get_context(request, profile_instance)

        categories = BusinessTaxonomy.get_categories()
        context.update({'categories': categories})

        return context


class CoreProfileEdit(views.ProfileEditView):

    form_profile = CoreUserProfileFullEditForm

    def get_context(self, request, profile_instance=None):

        states = BusinessUserProfile.get_states(1)
        cities = BusinessUserProfile.get_cities(profile_instance.city.state.id) if profile_instance.city else None
        responsibilities = BusinessUserProfile.get_responsibilities()
        categories = BusinessTaxonomy.get_categories()

        return {
            'states': states,
            'cities': cities,
            'categories': categories,
            'responsibilities': responsibilities
        }


class CoreProfileEditAjax(views.ProfileEditView):

    form_profile = CoreUserProfileEditForm

    def return_error(self, request, context=None):
        _response_context = {}

        if 'form' in context:
            _form = context['form']
            _response_context = {'errors': _form.errors}

        return JsonResponse(_response_context, status=400)

    def return_success(self, request, context=None):
        return JsonResponse(context, status=200)



class CoreProfileWizardStepOne(View):
    template_name = 'core/partials/wizard/wizard-step-one.html'
    form  = WizardFormStepOne

    def get_context(self, request):
        context = {}
        context['responsibilities'] = Responsibility.objects.all().\
            only("id", "name").order_by("name")

        return  context

    def get(self, request):

        context = self.get_context(request)
        return render(request, self.template_name, context)

class CoreProfileWizard(View):

    view_index = {
        1: CoreProfileWizardStepOne
    }


    @staticmethod
    def __get_valid_wizard_index__(index):
        return index if index and index > 0 else 1

    def __get_step_one__(self, request):
        template_name = 'core/partials/wizard/wizard-step-one.html'

        return render(request, template_name)

    def __get_step_two__(self, request):
        template_name = 'core/partials/wizard/wizard-step-two.html'

    def __get_step_three__(self, request):
        template_name = 'core/partials/wizard/wizard-step-three.html'


    def get(self, request, step):
        template_index = int(step) if step else 1

        user_step = self.__get_valid_wizard_index__(request.user.user_profile.wizard_step)
        if user_step != template_index:
            return redirect(to="profile:wizard", step=user_step)

        step_view = self.view_index[template_index]()

        return step_view.get(request)


class CoreProfileWizardStepTwoAjax(views.ProfileBaseView):

    template_segment_path = 'core/partials/wizard/community-segment.html'

    def return_error(self, request, context=None):
        if not context:
            context = {}

        _context = context

        return JsonResponse(_context, status=400)

    def return_success(self, request, context=None):
        if not context:
            context = {}
        _context = {}
        _context['page'] = context['page']
        _context['taxonomies'] = context['taxonomies']

        _context['template'] = render(request, self.template_segment_path, context).content

        return JsonResponse(_context, status=200)

    def get_context(self, request, profile_instance=None):
        profile = BusinessUserProfile.update_wizard_step(profile_instance, 2)
        return {'step': profile.wizard_step}

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        profile = self.filter(request, request.user)

        context = {}

        if 'taxonomies' not in request.GET:
            context.update({'status': 400})
            return self.return_error(request, context)


        form = CoreCommunityFormSearch(6, request.GET)
        communities = form.process()
        taxonomies = [taxonomy.id for taxonomy in form.cleaned_data['taxonomies']]

        context['status'] = 200
        context['taxonomies'] = taxonomies
        context['communities'] = communities
        context['page'] = form.cleaned_data['page'] + 1
        context['criteria'] = form.cleaned_data['criteria']

        context.update(self.get_context(request, profile))
        return self.return_success(request, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        profile = self.filter(request, request.user)

        context = {}
        context.update(self.get_context(request, profile))

        if 'taxonomies' in request.POST:
            taxonomy_categories_obj = BusinessTaxonomy.get_categories(request.POST.getlist('taxonomies'))
            taxonomy_communities = BusinessTaxonomy.get_related_list_top_down(taxonomy_categories_obj)
            taxonomies = [tax.id for tax in taxonomy_communities]



            communities = BusinessCommunity.get_category_communities(taxonomies)

            BusinnesSocialAction.set_follow_by_user_and_models(request.user, communities)

            form = CoreCommunityFormSearch(6, {"taxonomies": taxonomies})
            communities = form.process()

            context['status'] = 200
            context['taxonomies'] = taxonomies
            context['communities'] = communities
            context['page'] = communities.number + 1

            context['template'] = render(request, self.template_segment_path, {
                'communities': communities,
                'taxonomies': taxonomies,
                'page': communities.number + 1
            }).content

            return self.return_success(request, context)

        return self.return_error(request, context)


class CoreProfileWizardStepTwoListAjax(CoreProfileWizardStepTwoAjax):

    def return_error(self, request, context=None):

        pass

    def return_success(self, request, context=None):
        if not context:
            context = {}

        _context = context

        return render(request, self.template_segment_path, _context, status=200)

    def get_context(self, request, profile_instance=None):
        return {}


class CoreProfileWizardStepTwoListJSON(CoreProfileWizardStepTwoListAjax):

    def return_success(self, request, context=None):

        if not context:
            context = {}

        _context = context

        _context['template'] = render(request, self.template_segment_path, _context, status=200)

        return JsonResponse(_context, status=200)

    def get_context(self, request, profile_instance=None):
        return {}


class CoreProfileWizardStepThreeAjax(views.ProfileBaseView):

    def return_error(self, request, context=None):
        if not context:
            context = {}

        _context = context

        return JsonResponse(_context, status=400)

    def return_success(self, request, context=None):
        if not context:
            context = {}

        _context = context

        return JsonResponse(_context, status=200)

    def get_context(self, request, profile_instance=None):
        profile = BusinessUserProfile.update_wizard_step(profile_instance, 3)
        return {'step': profile.wizard_step}

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        profile = self.filter(request, request.user)
        context = {}

        if not profile:
            context.update({'status': 400})
            return self.return_error(request, context)

        context.update({'status': 200})
        context.update(self.get_context(request, profile))
        return self.return_success(request, context)


class CoreProfileFollowingsSearch(views.ProfileShowView):

    items_per_page = 9

    template_path = "userprofile/profile-followings.html"

    form = CoreSearchFollowings

    def get_context(self, request, profile_instance=None):

        form = self.form(
            profile_instance.user,
            self.items_per_page,
            request.GET
        )

        response = {}
        response_form = form.process()

        if response_form:
            response.update(response_form)

        return {
            'items': response.get('items'),
            'content_type': response.get('content_type'),
            'object': response.get('object'),
            'form': form,
            'page': form.cleaned_data.get('page', 0) + 1
        }


class CoreProfileFollowingsSearchList(CoreProfileFollowingsSearch):

    template_path = "userprofile/partials/followings-segment.html"


class CoreProfileFollowersSearch(views.ProfileShowView):

    items_per_page = 9

    template_path = "userprofile/profile-followers.html"

    form = CoreSearchFollowers

    def get_context(self, request, profile_instance=None):

        form = self.form(
            profile_instance.user,
            self.items_per_page,
            request.GET
        )

        response = {}
        response_form = form.process()

        if response_form:
            response.update(response_form)

        return {
            'items': response.get('items'),
            'content_type': response.get('content_type'),
            'object': response.get('object'),
            'form': form,
            'page': form.cleaned_data.get('page', 0) + 1
        }


class CoreProfileFollowersSearchList(CoreProfileFollowersSearch):

    template_path = "userprofile/partials/followers-segment.html"


class CoreProfileCommunitiesLoad(views.ProfileShowView):

    template_segment_path = "userprofile/partials/profile-community-list.html"

    def return_error(self, request, context=None):
        return render(request, self.template_segment_path, context)

    def return_success(self, request, context=None):
        return render(request, self.template_segment_path, context)

    def get_context(self, request, profile_instance=None):

        url_next = request.POST.get('url-next')

        communities = BusinessSocialActions.get_random_users_acted_by_author(
            author=profile_instance.user,
            action=settings.SOCIAL_FOLLOW,
            content_type='community',
            items_per_page=3,
            page=1
        )

        return {
            'communities': communities,
            'url_next': url_next
        }

    def get(self, request, username):

        profile = self.filter(request, username)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return self.return_success(request, context)


class CoreProfileCommunitiesLoadAjax(CoreProfileCommunitiesLoad):

    def return_error(self, request, context=None):
        return JsonResponse(context, status=400)

    def return_success(self, request, context=None):
        if not context:
            context = {}

        _context = {
            'url_next': context.get('url_next'),
            'template': render(request, self.template_segment_path, context).content
        }

        return JsonResponse(_context, status=200)


class CoreProfileFollowingsLoadAjax(views.ProfileShowView):

    template_segment_path = "userprofile/partials/profile-followings-list.html"

    def return_error(self, request, context=None):
        return JsonResponse(context, status=400)

    def return_success(self, request, context=None):
        if not context:
            context = {}

        _context = {
            'url_next': context.get('url_next'),
            'template': render(request, self.template_segment_path, context).content
        }

        return JsonResponse(_context, status=200)

    def get_context(self, request, profile_instance=None):

        url_next = request.POST.get('url-next')

        followings = BusinessSocialActions.get_random_users_acted_by_author(
            author=profile_instance.user,
            action=settings.SOCIAL_FOLLOW,
            content_type='user',
            items_per_page=3,
            page=1
        )

        return {
            'followings': followings,
            'url_next': url_next
        }

    def get(self, request, username):

        profile = self.filter(request, username)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return self.return_success(request, context)


class CoreProfileSearchEditPosts(views.ProfileBaseView):

    template_path = "userprofile/profile-edit-posts.html"

    form = CoreSearchArticlesForm

    def return_success(self, request, context=None):
        return render(request, self.template_path, context)

    def get(self, request):
        profile = self.filter(request, request.user)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return self.return_success(request, context)

    def get_context(self, request, profile_instance=None):
        form = self.form(request.user, 10, True, request.GET)

        posts = form.process()
        status = Article.STATUS_CHOICES

        have_posts = True if hasattr(posts, 'object_list') and posts.object_list else False

        return {
            'posts': posts,
            'have_posts': have_posts,
            'form': form,
            'status_list': status,
            'status': int(form.cleaned_data.get('status')) if form.cleaned_data.get('status') else None,
            'page': form.cleaned_data.get('page', 1) + 1
        }


class CoreProfileSearchEditPostsAjax(CoreProfileSearchEditPosts):

    template_path = "userprofile/partials/profile-edit-posts-segment.html"

    def return_success(self, request, context=None):
        response_context = {
            'status': 200,
            'have_posts': context.get('have_posts'),
            'template': render(request, self.template_path, context).content
        }

        return JsonResponse(response_context, status=200)


class CoreProfileSearchEditPostsList(CoreProfileSearchEditPosts):
    template_path = "userprofile/partials/profile-edit-posts-segment.html"


class CoreProfileSearchEditQuestions(views.ProfileBaseView):

    template_path = "userprofile/profile-edit-questions.html"
    form = CoreSearchQuestionsForm

    def return_success(self, request, context=None):
        return render(request, self.template_path, context)

    def get(self, request):
        profile = self.filter(request, request.user)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return self.return_success(request, context)

    def get_context(self, request, profile_instance=None):
        form = self.form(request.user, 10, request.GET)

        posts = form.process()
        status = Article.STATUS_CHOICES

        have_posts = True if hasattr(posts, 'object_list') and posts.object_list else False

        return {
            'posts': posts,
            'have_posts': have_posts,
            'form': form,
            'status_list': status,
            'status': int(form.cleaned_data.get('status')) if form.cleaned_data.get('status') else None,
            'page': form.cleaned_data.get('page', 1) + 1
        }


class CoreProfileSearchEditQuestionsAjax(CoreProfileSearchEditQuestions):
    template_path = "userprofile/partials/profile-edit-questions-segment.html"

    def return_success(self, request, context=None):
        response_context = {
            'status': 200,
            'have_posts': context.get('have_posts'),
            'template': render(request, self.template_path, context).content
        }

        return JsonResponse(response_context, status=200)


class CoreProfileSearchEditQuestionsList(CoreProfileSearchEditQuestions):
    template_path = "userprofile/partials/profile-edit-questions-segment.html"


class CoreProfileVideosSearch(views.ProfileBaseView):

    template_path = "userprofile/profile-videos.html"

    form_videos = CoreSearchVideosForm

    def return_error(self, request, context=None):
        pass

    def return_success(self, request, context=None):
        return render(request, self.template_path, context)

    def get_context(self, request, profile_instance=None):

        form = self.form_videos(profile_instance.user, 10, request.GET)

        videos = form.process()

        have_posts = True if hasattr(videos, 'object_list') and videos.object_list else False

        return {
            'feed_objects': videos,
            'have_posts': have_posts,
            'form': form,
            'page': form.cleaned_data.get('page', 1) + 1
        }

    def get(self, request, username):

        profile = self.filter(request, username)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return self.return_success(request, context)


class CoreProfileVideosView(CoreProfileVideosSearch):
    pass


class CoreProfileVideosList(CoreProfileVideosSearch):

    template_path = "userprofile/partials/profile-videos-list.html"


class CoreProfileCommunitiesSearchView(views.ProfileBaseView):

    template_path = "userprofile/profile-communities.html"
    template_path_segment = "userprofile/partials/profile-communities.html"

    form = CoreSearchCommunitiesForm

    def return_error(self, request, context=None):
        pass

    def return_success(self, request, context=None):
        if request.is_ajax():
            _context = {
                'template': render(request, 'userprofile/partials/profile-communities.html', context).content
            }
            return JsonResponse(_context, status=200)
        return render(request, self.template_path, context)

    def get_context(self, request, profile_instance=None):

        form = self.form(profile_instance.user, 9, request.GET)
        communities = form.process()
        categories = BusinessUserProfile.get_categories()

        return {
            'items': communities,
            'form': form,
            'page': form.cleaned_data.get('page', 1) + 1,
            'categories': categories
        }

    def get(self, request, username):

        profile = self.filter(request, username)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return self.return_success(request, context)


class CoreProfileCommunitiesSearchListView(CoreProfileCommunitiesSearchView):

    def return_success(self, request, context=None):
        return render(request, self.template_path_segment, context)


class CoreUserCommunitiesListAjax(View):

    @method_decorator(login_required)
    def get(self, request):
        filter_name = request.GET.get('name', False)
        if not filter_name:
            return JsonResponse({}, status=200)

        user_communities = BusinessSocialActions.get_users_acted_by_author(
            author=request.user,
            action=settings.SOCIAL_FOLLOW,
            content_type='community',
            items_per_page=None,
        )

        community_content_type = ContentTypeCached.objects.get(model='community')

        all_communities = Community.objects.filter(title__istartswith=filter_name)
        communities_objects = user_communities.filter(object_id__in=all_communities, content_type=community_content_type)

        communities = []

        for action in communities_objects:
            community = dict()
            community['name'] = action.content_object.title
            community['id'] = action.content_object.id
            communities.append(community)

        return JsonResponse(communities, status=200, safe=False)


class CoreProfileSocialActionsBase(View):

    template_path = ""
    items_per_page = 9

    def return_error(self, request, context=None):
        if request.is_ajax():
            return JsonResponse({'error': context.get('msg')}, status=400)

        raise Http404(context.get('msg'))

    def return_success(self, request, context=None):
        if request.is_ajax():
            _context = {
                'template': render(request, self.template_path, context).content
            }
            return JsonResponse(_context, status=200)

        return render(request, self.template_path, context)


class SocialActionSeeLater(CoreProfileSocialActionsBase):

    template_path = 'socialactions/see-later.html'
    template_path_partial = 'socialactions/partials/list.html'

    form = CoreSearchSocialActionsForm
    action = settings.SOCIAL_SEE_LATER

    @method_decorator(login_required)
    def get(self, request):

        form = self.form(self.action, self.items_per_page, request.GET)
        form.set_author(request.user)
        items = form.process()

        context = {
            'form': form,
            'items': items,
            'action': settings.SOCIAL_LABELS[self.action],
            'page': form.cleaned_data.get('page', 1) + 1,
            'url_next': request.GET.get('next'),
            'profile': request.user.profile
        }

        if request.is_ajax():
            self.template_path = self.template_path_partial

        return self.return_success(request, context)


class SocialActionSeeLaterList(SocialActionSeeLater):

    def return_success(self, request, context=None):
        return render(request, self.template_path_partial, context)


class SocialActionRemoveSeeLater(CoreProfileSocialActionsBase):
    form = CoreRemoveSocialActionForm
    action = settings.SOCIAL_SEE_LATER

    def return_error(self, request, context=None):
        return JsonResponse(context, status=400)

    def return_success(self, request, context=None):
        return JsonResponse(context, status=200)

    @method_decorator(login_required)
    def post(self, request):

        form = self.form(self.action, request.POST)
        form.set_author(request.user)
        if form.process():
            return self.return_success(request, {'removed_items': form.processed})

        return self.return_error(request, {'status': 400})


class SocialActionFavourite(CoreProfileSocialActionsBase):

    template_path = 'socialactions/favourite.html'
    template_path_partial = 'socialactions/partials/list.html'

    form = CoreSearchSocialActionsForm
    action = settings.SOCIAL_FAVOURITE

    @method_decorator(login_required)
    def get(self, request):

        form = self.form(self.action, self.items_per_page, request.GET)
        form.set_author(request.user)
        items = form.process()

        context = {
            'form': form,
            'items': items,
            'action': settings.SOCIAL_LABELS[self.action],
            'page': form.cleaned_data.get('page', 1) + 1,
            'url_next': request.GET.get('next'),
            'profile': request.user.profile
        }

        if request.is_ajax():
            self.template_path = self.template_path_partial

        return self.return_success(request, context)


class SocialActionFavouriteList(SocialActionFavourite):

    def return_success(self, request, context=None):
        return render(request, self.template_path_partial, context)


class SocialActionRemoveFavourite(CoreProfileSocialActionsBase):
    form = CoreRemoveSocialActionForm
    action = settings.SOCIAL_FAVOURITE

    def return_error(self, request, context=None):
        return JsonResponse(context, status=400)

    def return_success(self, request, context=None):
        return JsonResponse(context, status=200)

    @method_decorator(login_required)
    def post(self, request):

        form = self.form(self.action, request.POST)
        form.set_author(request.user)
        if form.process():
            return self.return_success(request, {'removed_items': form.processed})

        return self.return_error(request, {'status': 400})


class SocialActionSuggest(CoreProfileSocialActionsBase):

    template_path = 'socialactions/suggest.html'
    template_path_partial = 'socialactions/partials/list.html'

    form = CoreSearchSocialActionsForm
    action = settings.SOCIAL_SUGGEST

    @method_decorator(login_required)
    def get(self, request):

        form = self.form(self.action, self.items_per_page, request.GET)
        form.set_target_user(request.user)
        items = form.process()

        context = {
            'form': form,
            'items': items,
            'action': settings.SOCIAL_LABELS[self.action],
            'page': form.cleaned_data.get('page', 1) + 1,
            'url_next': request.GET.get('next'),
            'profile': request.user.profile
        }

        if request.is_ajax():
            self.template_path = self.template_path_partial

        return self.return_success(request, context)


class SocialActionSuggestList(SocialActionSuggest):

    def return_success(self, request, context=None):
        return render(request, self.template_path_partial, context)


class SocialActionRemoveSuggest(CoreProfileSocialActionsBase):
    form = CoreRemoveSocialActionForm
    action = settings.SOCIAL_SUGGEST

    def return_error(self, request, context=None):
        return JsonResponse(context, status=400)

    def return_success(self, request, context=None):
        return JsonResponse(context, status=200)

    @method_decorator(login_required)
    def post(self, request):

        form = self.form(self.action, request.POST)
        form.set_target_user(request.user)
        if form.process():
            return self.return_success(request, {'removed_items': form.processed})

        return self.return_error(request, {'status': 400})


class SocialActionListItems(CoreProfileSocialActionsBase):

    template_path = 'socialactions/partials/list.html'

    form = CoreSearchSocialActionsForm
    items_per_page = 10

    def return_success(self, request, context=None):
        return render(request, self.template_path, context)

    @method_decorator(login_required)
    def get(self, request, action):

        action = BusinessSocialActions.get_by_label(action)

        form = self.form(action, self.items_per_page, request.GET)

        if action == settings.SOCIAL_SUGGEST:
            form.set_target_user(request.user)
        else:
            form.set_author(request.user)

        items = form.process()

        context = {
            'form': form,
            'items': items,
            'action': settings.SOCIAL_LABELS[action],
            'page': form.cleaned_data.get('page', 1) + 1,
            'url_next': request.GET.get('next'),
            'profile': request.user.profile
        }

        return self.return_success(request, context)


class CoreUserMyQuestions(CoreUserView):

    template_path = 'userprofile/profile-questions.html'
    form = CoreUserMyQuestionsForm

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        return super(CoreUserMyQuestions, self).get(request)

    def get_context(self, request, profile_instance=None):
        content_type = ContentTypeCached.objects.get(model='question')

        itens_by_page = 5

        form = self.form(
            profile_instance,
            content_type.id,
            itens_by_page,
            profile_instance.user,
            request.GET
        )

        feed_objects = form.process()

        return {
            'feed_objects': feed_objects,
            'form': form,
            'page': form.cleaned_data.get('page', 0) + 1
        }


class CoreUserMyQuestionsList(CoreUserMyQuestions):

    template_path = 'userprofile/partials/profile-questions-list.html'


