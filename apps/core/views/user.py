# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.shortcuts import render
from django_thumbor import generate_url
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

from apps.community.models import Community
from apps.core.forms.user import CoreUserProfileForm, CoreUserProfileFullEditForm, CoreSearchFollowers, CoreSearchArticlesForm, CoreSearchVideosForm, \
    CoreSearchCommunitiesForm, CoreSearchFavouriteForm, CoreRemoveSocialActionForm
from apps.core.forms.community import CoreCommunityFormSearch
from apps.core.forms.user import CoreUserSearchForm, CoreUserProfileEditForm
from apps.article.models import Article
from apps.userprofile import views
from apps.userprofile.service import business as BusinessUserprofile
from apps.taxonomy.service import business as BusinessTaxonomy
from apps.socialactions.service import business as BusinessSocialActions
from apps.core.business import socialactions as Business
from apps.core.forms.user import CoreSearchFollowings
from apps.socialactions.localexceptions import NotFoundSocialSettings
from apps.userprofile.service import business as BusinessUserProfile
from rede_gsti import settings


class CoreUserView(views.ProfileShowView):

    template_path = 'userprofile/profile.html'
    form = CoreUserSearchForm

    def get_context(self, request, profile_instance=None):
        context = super(CoreUserView, self).get_context(request, profile_instance)

        itens_by_page = 5

        form = self.form(
            profile_instance,
            ['article', 'question'],
            itens_by_page,
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

    template_path = 'userprofile/partials/user-profile-list.html'

    def get(self, request, username=None):

        profile = self.filter(request, username)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return render(request, self.template_path, context)


class CoreUserProfile(CoreUserView):
    template_path = 'userprofile/profile-list.html'
    form = CoreUserProfileForm

    def get(self, request, username=None):

        profile = self.filter(request, username)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return render(request, self.template_path, context)

    def get_context(self, request, profile_instance=None):
        content_type = ContentType.objects.filter(model='article')

        itens_by_page = 5

        form = self.form(
            profile_instance,
            content_type.first().id,
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

        itens_by_page = 5
        content_type = ContentType.objects.filter(model='article')

        form = self.form(
            profile_instance,
            content_type.first().id,
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


class CoreUserFeed(CoreUserView):
            
    template_path = 'userprofile/profile-feed.html'

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        return super(CoreUserFeed, self).get(request)

    def get_context(self, request, profile_instance=None):
        context = super(CoreUserFeed, self).get_context(request, profile_instance)

        states = BusinessUserprofile.get_states(1)
        cities = BusinessUserprofile.get_cities(profile_instance.city.state.id) if profile_instance.city else None
        responsibilities = BusinessUserprofile.get_responsibilities()
        categories = BusinessTaxonomy.get_categories()

        context.update({
            'states': states,
            'cities': cities,
            'categories': categories,
            'responsibilities': responsibilities
        })
        return context


class CoreProfileEdit(views.ProfileEditView):

    form_profile = CoreUserProfileFullEditForm

    def get_context(self, request, profile_instance=None):

        states = BusinessUserprofile.get_states(1)
        cities = BusinessUserprofile.get_cities(profile_instance.city.state.id) if profile_instance.city else None
        responsibilities = BusinessUserprofile.get_responsibilities()
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


class CoreProfileWizardStepOneAjax(CoreProfileEditAjax):

    def get_context(self, request, profile_instance=None):
        profile = BusinessUserprofile.update_wizard_step(profile_instance, 1)
        return {'step': profile.wizard_step}


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

        _context['template'] = render(request, self.template_segment_path, {
            'communities': context['communities'],
            'taxonomies': context['taxonomies'],
            'page': context['page']
        }).content

        return JsonResponse(_context, status=200)

    def get_context(self, request, profile_instance=None):
        profile = BusinessUserprofile.update_wizard_step(profile_instance, 2)
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
        profile = BusinessUserprofile.update_wizard_step(profile_instance, 3)
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

    def post(self, request, username):

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

    def post(self, request, username):

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

        community_content_type = ContentType.objects.get(model='community')

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

    @method_decorator(login_required)
    def get(self, request):

        criteria = None
        if 'criteria' in request.GET:
            criteria = str(request.GET['criteria'])
            self.template_path = 'socialactions/partials/see-later.html'

        try:
            content = Business.get_see_later_content(request.user, criteria)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (content.number if content and content.number else 0) + 1,
            'criteria': self.template_path,
            'profile': request.user.profile
        }

        return self.return_success(request, context)


class SocialActionRemoveSeeLater(CoreProfileSocialActionsBase):
    template_path = 'socialactions/see-later.html'

    @method_decorator(login_required)
    def post(self, request):

        itens_to_remove = request.POST.getlist(u'itens_to_remove[]')
        try:
            content = Business.remove_see_later_content(user=request.user, itens_to_remove=itens_to_remove)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (content.page if content.page and content.page else 0) + 1,
            'criteria': self.template_path,
            'profile': request.user.profile
        }

        return self.return_success(request, context)


class SocialActionFavourite(CoreProfileSocialActionsBase):

    template_path = 'socialactions/favourite.html'
    template_path_partial = 'socialactions/partials/favourite.html'

    form = CoreSearchFavouriteForm

    @method_decorator(login_required)
    def get(self, request):

        form = self.form(request.user, 9, request.GET)
        items = form.process()

        context = {
            'form': form,
            'items': items,
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
    template_path = 'socialactions/favourite.html'

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

    @method_decorator(login_required)
    def get(self, request):

        criteria = None
        if 'criteria' in request.GET:
            criteria = str(request.GET['criteria'])
            self.template_path = 'socialactions/partials/suggest.html'

        try:
            content = Business.get_suggest_content(request.user, criteria)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (content.number if content and content.number else 0) + 1,
            'criteria': self.template_path,
            'profile': request.user.profile
        }

        return self.return_success(request, context)


class SocialActionSuggestList(SocialActionSuggest):

    def return_success(self, request, context=None):
        return render(request, 'socialactions/partials/suggest.html', context)


class SocialActionRemoveSuggest(CoreProfileSocialActionsBase):
    template_path = 'socialactions/partials/suggest.html'

    @method_decorator(login_required)
    def post(self, request):

        itens = request.POST.getlist('itens_to_remove[]')
        itens_to_remove = []

        for item in itens:
            itens_to_remove.append(int(item))

        try:
            content = Business.remove_suggest_content(user=request.user, itens_to_remove=itens_to_remove)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.')
            }
            return self.return_error(request, context)

        return JsonResponse({'removedItens': content}, status=200)