import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.core.forms.user import CoreUserSearchForm
from apps.userprofile import views
from apps.userprofile.service import business as BusinessUserprofile


class CoreUserSearchView(views.ProfileShowView):

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

    def get(self, request, **kwargs):

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

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        return super(CoreUserFeed, self).get(request)

    def get_context(self, request, profile_instance=None):
        context = super(CoreUserFeed, self).get_context(request, profile_instance)

        states = BusinessUserprofile.get_states(1)

        context.update({'states': states})

        return context


class CoreProfileEditAjax(views.ProfileEditView):

    def return_success(self, request, context=None):
        print context
        return json.dumps(context)