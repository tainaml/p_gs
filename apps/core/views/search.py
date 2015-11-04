from django.shortcuts import render
from django.views.generic import View

from ..forms import search as Forms

class SearchBase(View):

    template_path = ""

    form_community = Forms.SearchCommunityForm
    form_user = Forms.SearchUserForm
    form_article = Forms.SearchArticleForm
    form_question = Forms.SearchQuestionForm

    def return_error(self, request, context):
        return render(request, self.template_path, context)

    def return_success(self, request, context):
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
            print e
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
            'query_search': request.GET.get('q')
        }
        context.update(self.get_context(request))

        return self.return_success(request, context)


class SearchAutocomplete(SearchBase):

    def return_error(self, request, context):
        pass

    def return_success(self, request, context):
        pass