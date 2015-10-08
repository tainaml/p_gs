from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from apps.core.forms.user import CoreUserSearchForm, CoreUserProfileForm
from apps.userprofile.views import ProfileShowView


class CoreUserView(ProfileShowView):

    template_path = 'userprofile/profile.html'
    form = CoreUserSearchForm

    def get_context(self, request, profile_instance=None):
        context = super(
            CoreUserView,
            self
        ).get_context(
            request,
            profile_instance
        )

        itens_by_page = 10

        form = self.form(
            profile_instance,
            ['article', 'question'],
            itens_by_page,
            request.user,
            request.GET
        )

        feed_objects = form.process()

        context.update(
            {'feed_objects': feed_objects,
            'form': form,
            'page': form.cleaned_data['page'] + 1
        })

        return context

    def get(self, request, username=None):

        profile = self.filter(request, request.user)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return render(request, self.template_path, context)


class CoreUserList(CoreUserView):
    template_path = 'userprofile/partials/profile-list.html'

    def get_context(self, request, profile_instance=None):
        context = super(CoreUserView, self).get_context(request, profile_instance)

        return context


class CoreUserFeed(CoreUserView):
    template_path = 'userprofile/profile-feed.html'


class CoreUserProfile(CoreUserView):
    template_path = 'userprofile/profile.html'
    form = CoreUserProfileForm

    def get(self, request, username=None):

        profile = self.filter(request, username)

        context = {'profile': profile}
        context.update(self.get_context(request, profile))

        return render(request, self.template_path, context)

    def get_context(self, request, profile_instance=None):
        content_type = ContentType.objects.filter(model='article')

        itens_by_page = 10

        form = self.form(
            profile_instance,
            content_type[0].id,
            itens_by_page,
            profile_instance.user,
            request.GET
        )

        feed_objects = form.process()

        return {
            'feed_objects': feed_objects,
            'form': form,
            'page': form.cleaned_data['page'] + 1
        }


class CoreUserSearch(CoreUserView):
    template_path = 'userprofile/profile-search.html'