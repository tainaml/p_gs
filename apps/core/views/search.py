#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from apps.taxonomy.models import Taxonomy, Term
from apps.userprofile.service import business as BusinessUserProfile

from ..forms import search as Forms
import urllib

class SearchBase(View):

    template_path = ""

    form_community = Forms.SearchCommunityForm
    form_user = Forms.SearchUserForm
    form_article = Forms.SearchArticleForm
    form_question = Forms.SearchQuestionForm

    def return_error(self, request, context=None):
        return render(request, self.template_path, context)

    def return_success(self, request, context=None):
        return render(request, self.template_path, context)

    def get_context(self, request, *args, **kwargs):
        return {}


class Search(SearchBase):

    template_path = "search/search-result.html"

    def get(self, request):

        form_community = self.form_community(6, False, request.GET)
        form_user = self.form_user(6, False, request.GET)
        form_article = self.form_article(6, False, request.GET)
        form_question = self.form_question(6, False, request.GET)

        try:
            communities = form_community.process()
            users = form_user.process()
            articles = form_article.process()
            questions = form_question.process()
            states = BusinessUserProfile.get_states(1)
        except Exception, e:
            return self.return_error(request, {})

        context = {
            'communities': communities,
            'users': users,
            'articles': articles,
            'questions': questions,
            'form_community': form_community,
            'form_user': form_user,
            'form_article': form_article,
            'form_question': form_question,
            'query_search': request.GET.get('q'),
            'states': states
        }
        context.update(self.get_context(request))

        return self.return_success(request, context)


class SearchAutocomplete(SearchBase):

    template_path = "search/partials/search-autocomplete.html"

    def return_error(self, request, context=None):
        pass

    def return_success(self, request, context=None):
        if not context:
            context = {}

        _context = {
            'template': render(request, self.template_path, context).content
        }

        if request.is_ajax():
            return JsonResponse(_context, status=200)

    def get(self, request):

        form_community = self.form_community(3, True, request.GET)
        form_user = self.form_user(3, True, request.GET)

        try:
            communities_filtered = form_community.process()
            users_filtered = form_user.process()
        except Exception, e:
            return self.return_error(request, {})

        context = {
            'communities': communities_filtered,
            'users': users_filtered,
            'form_community': form_community,
            'form_user': form_user,
            'query_search': request.GET.get('q')
        }
        context.update(self.get_context(request))

        return self.return_success(request, context)


class SearchList(SearchBase):

    def return_error(self, request, context=None):
        return HttpResponse('', status=200)

    def return_success(self, request, context=None):
        return render(request, self.template_path, context)

    def change_template(self, template_path):
        self.template_path = template_path

    def get(self, request, content_type):

        context = {}

        __category = request.GET.get('category', None)

        context.update({'content_type': content_type})

        if __category:
            try:
                term = Term.objects.get(slug="categoria")
                category = Taxonomy.objects.get(slug=__category, term=term)
                context.update({"category":category.slug})
            except Exception, e:
                print e.message

        try:

            if content_type == "communities":
                form = self.form_community(6, False, request.GET)
                communities = form.process()
                categories = BusinessUserProfile.get_categories()
                context.update({
                    'communities': communities,
                    'form_community': form,
                    'categories': categories,
                    'profile': request.user.profile
                })

            elif content_type == "users":
                form = self.form_user(6, False, request.GET)
                states = BusinessUserProfile.get_states(1)
                users = form.process()
                context.update({
                    'users': users,
                    'form_user': form,
                    'states': states,
                })

            elif content_type == "articles":
                form = self.form_article(6, False, request.GET)
                articles = form.process()
                context.update({
                    'articles': articles,
                    'form_article': form,
                })

            elif content_type == "questions":
                form = self.form_question(6, False, request.GET)
                questions = form.process()
                context.update({
                    'questions': questions,
                    'form_question': form,
                })

            else:
                raise Exception("Content Type is not found.")

        except Exception, e:
            return self.return_error(request, {})

        context.update({
            'page': form.cleaned_data.get('page', 1) + 1,
            'query_search': request.GET.get('q', None)
        })
        context.update(self.get_context(request))

        self.change_template("search/partials/search-%s.html" % content_type)

        return self.return_success(request, context)


class SearchContent(SearchList):

    template_path = "search/search-result.html"

    def change_template(self, template_path):
        return self.template_path


class SearchCommunitiesList(SearchBase):

    form_community = Forms.SearchCommunityForm

    def change_template(self, template_path):
        self.template_path = template_path

    def create_pagination(self, communities):
        return Paginator(communities, 6)

    def get(self, request):
        context = {}

        try:
            form = self.form_community(6, False, request.GET)
            communities = form.process()
            paginated_communities = self.create_pagination(communities)
            categories = BusinessUserProfile.get_categories()
            context.update({
                'communities': communities,
                'form_community': form,
                'categories': categories,
                'items': paginated_communities.object_list,
                'profile': request.user.profile
            })

        except Exception, e:
            return self.return_error(request, {})

        context.update({
            'page': form.cleaned_data.get('page', 1) + 1,
            'query_search': request.GET.get('q')
        })
        context.update(self.get_context(request))

        self.change_template("search/partials/search-communities.html")

        return self.return_success(request, context)

def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            v.decode('utf8')
        out_dict[k] = v
    return out_dict

class SearchAll(View):
    def get(self, request, params):
        querystring = {'q': params}
        return redirect(reverse("search:search")+"?%s" % urllib.urlencode(encoded_dict(querystring)))
