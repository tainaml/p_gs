from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from apps.userprofile.service import business as BusinessUserProfile

from ..forms import search as Forms


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

        try:

            if content_type == "communities":
                form = self.form_community(6, False, request.GET)
                communities = form.process()

                categories = BusinessUserProfile.get_categories()
                context.update({
                    'communities': communities,
                    'form_community': form,
                    'categories':categories,
                })

            elif content_type == "users":
                form = self.form_user(6, False, request.GET)
                users = form.process()
                context.update({
                    'users': users,
                    'form_user': form,
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
            'query_search': request.GET.get('q')
        })
        context.update(self.get_context(request))

        self.change_template("search/partials/search-%s.html" % content_type)

        return self.return_success(request, context)


class SearchContent(SearchList):

    template_path = "search/search-result.html"

    def change_template(self, template_path):
        return self.template_path
