#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import urllib
from django.core.urlresolvers import reverse
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from apps.community import views
from apps.community.models import Community
from apps.community.service import business as Business
from apps.core.forms.community import CoreCommunityFeedFormSearch, CoreCommunityQuestionFeedFormSearch, \
    CoreCommunitySearchVideosForm, CoreCommunityFollowersForm, CoreCommunitySearchMaterialsForm, CoreCommunityGetAllForm
from apps.core.forms.course import CourseCommunityListForm
from apps.core.forms.ranking import RankingListForm
from apps.core.views.course import CourseListView
from apps.core.views.search import encoded_dict
from apps.custom_base.views import FormBaseListView, FormBasePaginetedListView
from apps.socialactions.service.business import get_users_acted_by_model
from rede_gsti import settings
from apps.core.business import community as BusinessCommunity
from apps.userprofile.service import business as BusinessUserProfile


class CoreCommunityView(views.CommunityView):

    template_path = 'community/community-view.html'

    def get_context(self, request, community_instance=None):

        if request.user and request.user.is_authenticated():

            if isinstance(community_instance, Community):
                community_followers = get_users_acted_by_model(model=community_instance,
                                                               action=settings.SOCIAL_FOLLOW,
                                                               filter_parameters={'author': request.user},
                                                               itens_per_page=20,
                                                               page=1)

                return {'user_follows_community': community_followers}

        return {}


class CoreCommunityFollowersView(CoreCommunityView):

    template_path = 'community/community-followers.html'

    def get_context(self, request, community_instance=None):

        states = BusinessUserProfile.get_states(1)
        return {'states': states}


class CoreCommunityAboutView(CoreCommunityView):

    template_path = 'community/community-about.html'


class CoreCommunitySearch(CoreCommunityView):

    template_path = 'community/community-view.html'

    def get_context(self, request, community_instance=None):
        context = super(CoreCommunitySearch, self).get_context(request, community_instance)
        itens_by_page = 10

        self.form = CoreCommunityFeedFormSearch(
            community_instance,
            ['article', 'question'],
            itens_by_page,
            request.GET
        )
        feed_objects = self.form.process()

        context.update({'feed_objects': feed_objects, 'form': self.form, 'page': self.form.cleaned_data['page'] + 1})

        return context


class CoreCommunityFeedView(CoreCommunitySearch):


    def get_context(self, request, community_instance=None):
        context = super(CoreCommunityFeedView, self).get_context(request, community_instance)
        context.update({
            'from_root_category': bool(community_instance.taxonomy.term.slug == 'categoria')
        })

        return context


    def get(self, request, community_slug):
        community = Business.get_community(slug=community_slug)
        if request.is_ajax():
            self.template_path = 'community/partials/community-list.html'
        else:
            self.template_path = 'community/community-view.html'

        if not community:
            querystring = {'q': community_slug}
            return redirect(reverse("search:search")+"?%s" % urllib.urlencode(encoded_dict(querystring)))

        return super(CoreCommunityFeedView, self).get(request, community_slug)


class CoreCommunityCourses(CourseListView):

    form = CourseCommunityListForm
    community = None
    itens_per_page = 9

    success_template_path = 'community/community-courses.html'
    success_ajax_template_path = 'community/partials/community-course-items.html'
    fail_validation_template_path = success_ajax_template_path

    def after_process(self, request=None, *args, **kwargs):
        super(CoreCommunityCourses, self).after_process(request, *args, **kwargs)
        self.context.update({'community': self.community})

    def after_fill(self, request, *args, **kwargs):
        self.form.set_community(self.community)

    def get(self, request=None, community_slug=None, *args, **kwargs):
        try:
            self.community = Community.objects.get(slug=community_slug)

        except Community.DoesNotExist:
            raise Http404()


        return self.do_process(request, *args, **kwargs)



class CoreCommunityQuestionSearch(CoreCommunityView):

    template_path = 'community/community-questions.html'

    def get_context(self, request, community_instance=None):
        context = super(CoreCommunityQuestionSearch, self).get_context(request, community_instance)
        itens_by_page = 3

        self.form = CoreCommunityQuestionFeedFormSearch(
            community_instance,
            ['question'],
            itens_by_page,
            request.GET
        )
        feed_objects = self.form.process()

        context.update({'feed_objects': feed_objects, 'form': self.form, 'page': self.form.cleaned_data['page'] + 1})

        return context


class CoreCommunityQuestionFeedView(CoreCommunityQuestionSearch):

    template_path = 'community/community-questions.html'
    
    def get(self, request, community_slug):

        if request.is_ajax():
            self.template_path = 'community/partials/community-question-list.html'

        return super(CoreCommunityQuestionFeedView, self).get(request, community_slug)



class CoreCommunityQuestionList(CoreCommunityQuestionSearch):

    template_path = 'community/partials/community-question-list.html'

    def get_context(self, request, community_instance=None):
        context = super(CoreCommunityQuestionList, self).get_context(request, community_instance)

        return context


class CoreCommunityVideosSearch(views.CommunityView):

    template_path = "community/community-videos.html"

    form_videos = CoreCommunitySearchVideosForm

    def return_error(self, request, context=None):
        pass

    def return_success(self, request, context=None):
        return render(request, self.template_path, context)

    def get_context(self, request, community_instance=None):

        form = self.form_videos(community_instance, 3, request.GET)

        videos = form.process()
        have_posts = True if hasattr(videos, 'object_list') and videos.object_list else False

        return {
            'feed_objects': videos,
            'have_posts': have_posts,
            'form': form,
            'page': form.cleaned_data.get('page', 1) + 1
        }


class CoreCommunityVideosView(CoreCommunityVideosSearch):
    template_path = "community/community-videos.html"

    def get(self, request, community_slug):

        if request.is_ajax():
            self.template_path = "community/partials/community-videos-list.html"


        return super(CoreCommunityVideosSearch, self).get(request, community_slug)


class CoreCommunityVideosList(CoreCommunityVideosSearch):

    template_path = "community/partials/community-videos-list.html"



class CoreGetCommunities(views.View):

    form = CoreCommunityGetAllForm
    itens_per_page = 6

    def get(self, request):


        form = self.form(self.itens_per_page, request.GET)

        communities = form.process() if form.is_valid() else []

        return JsonResponse({'communities': communities})




class CoreCommunityLoad(views.View):

    template_path = ""

    def return_error(self, request, context=None):
        pass

    def return_success(self, request, context=None):
        if not context:
            context = {}

        if request.is_ajax():
            _context = {
                'template': render(request, self.template_path, context).content
            }
            return JsonResponse(_context, status=200)

    def change_template(self, template_path):
        self.template_path = template_path

    def get_context(self, request, *args, **kwargs):
        return {}

    def get(self, request, object_id, content_type):

        url_next = request.POST.get('url-next')

        communities = BusinessCommunity.get_random_communities_by_article_or_question(
            object_id=object_id,
            content_type=content_type
        )

        context = {
            'communities': communities,
            'url_next': url_next
        }
        context.update(self.get_context(request))

        self.change_template("%s/partials/%s-community-list.html" % (content_type, content_type))

        return self.return_success(request, context)


class CoreCommunityFollowersSearch(FormBaseListView):
    form = CoreCommunityFollowersForm
    success_template_path = "community/partials/community-followers-list.html"
    fail_template_path = success_template_path

    MAXIMUM_PER_PAGE = 6

    # @Override
    def after_process(self, request=None, *args, **kwargs):
        page = 1
        if 'page' in request.GET and request.GET.get('page').isdigit():

            page = int(request.GET.get('page')) + 1

        self.context.update({'community': request.GET['community'],'followers': self.process_return, 'page': page})

    # @Override
    def fill_form_kwargs(self, request=None, *args, **kwargs):
        return {'data': request.GET, 'items_per_page': self.MAXIMUM_PER_PAGE}


# class CoreCommunityFollowersSearch(views.CommunityBaseView):
#
#     template_path = "community/partials/community-followers-list.html"
#
#     form = CoreCommunityFollowersForm
#
#     def return_success(self, request, context=None):
#         if request.is_ajax():
#             _context = {
#                 'template': render(request, self.template_path, context).content
#             }
#             return JsonResponse(_context, status=200)
#
#         return render(request, self.template_path, context)
#
#     def get(self, request):
#
#         form = self.form(False, 6, request.GET)
#         followers = form.process()
#
#         context = {
#             'followers': followers,
#             'form': form,
#             'url_next': request.GET.get('next', '')
#         }
#         context.update(self.get_context(request))
#
#         return self.return_success(request, context)
#
#     def get_context(self, request):
#         return {}


class CoreCommunityFollowersSearchList(CoreCommunityFollowersSearch):

    def return_success(self, request, context=None):
        return render(request, self.template_path, context)


class CommunityRelated(CoreCommunityView):

    template_path = "community/partials/community-related.html"

    def get(self, request, community_slug=None):
        communities = BusinessCommunity.get_related_communities(community_slug)

        context = {'communities': communities}

        return JsonResponse({'template':render(request, self.template_path, context).content})


class CommunityCheckUserFollows(views.View):

    def post(self, request):

        community = Business.get_community(request.POST.get('community'))

        if not community:
            return JsonResponse({'msg': 'Community not found!'}, status=400)

        follows_community = get_users_acted_by_model(
            model=community,
            action=settings.SOCIAL_FOLLOW,
            filter_parameters={'author': request.user},
            itens_per_page=5,
            page=1
        )

        follows = True if follows_community else False

        return JsonResponse({'follows': follows}, status=200)


# Materials
class CoreCommunityMaterialsSearch(views.CommunityView):

    template_path = "community/community-materials.html"

    form_materials = CoreCommunitySearchMaterialsForm

    def return_error(self, request, context=None):
        pass

    def return_success(self, request, context=None):
        return render(request, self.template_path, context)

    def get_context(self, request, community_instance=None):

        form = self.form_materials(community_instance, 3, request.GET)

        posts = form.process()
        if request.is_ajax():
            self.template_path = "community/partials/community-materials-list.html"

        have_posts = True if hasattr(posts, 'object_list') and posts.object_list else False

        current_tag = form.cleaned_data.get('tags', None)
        if not current_tag:
            current_tag = request.GET.get('tags', None)

        return {
            'feed_objects': posts,
            'have_posts': have_posts,
            'tags': form.get_avaiable_tags(),
            'form': form,
            'current_tag': current_tag,
            'page': form.cleaned_data.get('page', 1) + 1
        }


class CoreCommunityMaterialsView(CoreCommunityMaterialsSearch):
    pass


class CoreCommunityMaterialsList(CoreCommunityMaterialsSearch):

    template_path = "community/partials/community-materials-list.html"


class CoreCommunityRanking(FormBasePaginetedListView):

    success_template_path = 'community/community-ranking.html'
    success_ajax_template_path = 'ranking/ranking-list.html'
    fail_validation_template_path = 'ranking/ranking-list.html'
    form = RankingListForm
    itens_per_page = 50



    def fill_form_kwargs(self, request=None, *args, **kwargs):
        data = copy.copy(request.GET)
        data['community'] = self.community.slug
        return {'data': data, 'itens_per_page': self.itens_per_page}

    # @Override
    def after_process(self, request=None, *args, **kwargs):
        super(CoreCommunityRanking, self).after_process(*args, **kwargs)
        self.context.update({'list': self.process_return, 'form': self.form,
                             'community': self.community, 'top_itens': self.itens_per_page * (self.context['page']-1) })

    def get(self, request=None, community_slug=None, *args, **kwargs):
        try:
            self.community = Community.objects.get(slug=community_slug)
        except Community.DoesNotExist:
            raise Http404()


        return self.do_process(request, *args, **kwargs)