from django.http import Http404
from django.shortcuts import render
from apps.core.forms.user import CoreUserSearchForm
from apps.userprofile.views import ProfileShowView


class CoreUserSearchView(ProfileShowView):

    template_path = 'userprofile/profile.html'

    def get_context(self, request, profile_instance=None):
        context = super(CoreUserSearchView, self).get_context(request, profile_instance)
        itens_by_page = 10

        self.form = CoreUserSearchForm(
            profile_instance,
            ['article', 'question'],
            itens_by_page,
            request.GET
        )

        feed_objects = self.form.process()

        context.update({'feed_objects': feed_objects, 'form': self.form, 'page': self.form.cleaned_data['page'] + 1})

        return context

    def get(self, request):

        profile = self.filter(request, request.user)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return render(request, self.template_path, context)


class CoreUserList(CoreUserSearchView):
    template_path = 'userprofile/partials/profile-list.html'

    def get_context(self, request, profile_instance=None):
        context = super(CoreUserSearchView, self).get_context(request, profile_instance)

        return context


class CoreUserFeed(CoreUserSearchView):
    template_path = 'userprofile/profile.html'