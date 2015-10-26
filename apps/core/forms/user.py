from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from custom_forms.custom import IdeiaForm, forms
from ..business import user as Business

from apps.article.models import Article
from apps.userprofile.models import Responsibility, State
from apps.userprofile.service import business as BusinessUserProfile
from apps.userprofile.service.forms import EditProfileForm


class CoreUserSearchForm(IdeiaForm):

    criterio = forms.CharField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, profile_instance=None, content_types=None,
        itens_by_page=None, user=None, *args, **kwargs):

        self.profile_instance=profile_instance
        self.content_types = content_types
        self.itens_by_page = itens_by_page
        self.user = user

        super(CoreUserSearchForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CoreUserSearchForm, self).clean()

        cleaned_data['page'] = cleaned_data['page']\
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):
        return Business.get_feed_objects(
            self.profile_instance,
            self.cleaned_data['criterio'],
            self.content_types,
            self.itens_by_page,
            self.cleaned_data['page'],
            self.user
        )


class CoreUserProfileForm(CoreUserSearchForm):

    def __process__(self):
        return Business.get_articles_from_user(
            profile_instance=self.profile_instance,
            description=self.cleaned_data['criterio'],
            content_type=self.content_types,
            items_per_page=self.itens_by_page,
            page=self.cleaned_data['page']
        )


class CoreUserProfileEditForm(EditProfileForm):

    responsibility = forms.ModelChoiceField(queryset=Responsibility.objects.all())
    state = forms.ModelChoiceField(queryset=State.objects.filter(country=1))

    @transaction.atomic()
    def __process__(self):
        process_profile = super(CoreUserProfileEditForm, self).__process__()
        process_occupation = BusinessUserProfile.create_occupation(process_profile, data={
            'responsibility': self.cleaned_data['responsibility']
        })

        return process_profile if (process_profile and process_occupation) else False


class CoreUserProfileFullEditForm(EditProfileForm):

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    responsibility = forms.ModelChoiceField(queryset=Responsibility.objects.all())
    state = forms.ModelChoiceField(queryset=State.objects.filter(country=1))

    @transaction.atomic()
    def __process__(self):
        process_profile = super(CoreUserProfileFullEditForm, self).__process__()
        process_user = BusinessUserProfile.update_user(self.user, data={
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name']
        })
        process_occupation = BusinessUserProfile.create_occupation(process_profile, data={
            'responsibility': self.cleaned_data['responsibility']
        })

        return process_profile if (process_profile and process_occupation and process_user) else False


class CoreSearchFollowings(IdeiaForm):

    criteria = forms.CharField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, author, items_per_page=None, *args, **kwargs):
        self.author = author
        self.items_per_page = items_per_page
        super(CoreSearchFollowings, self).__init__(*args, **kwargs)


    def clean(self):

        cleaned_data = super(CoreSearchFollowings, self).clean()
        cleaned_data['page'] = cleaned_data['page'] if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data


    def __process__(self):
        return Business.get_followings(
            self.author,
            self.cleaned_data['criteria'],
            self.items_per_page,
            self.cleaned_data.get('page', 0)
        )


class CoreSearchFollowers(IdeiaForm):

    criteria = forms.CharField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, author, items_per_page=None, *args, **kwargs):
        self.author = author
        self.items_per_page = items_per_page
        super(CoreSearchFollowers, self).__init__(*args, **kwargs)


    def clean(self):

        cleaned_data = super(CoreSearchFollowers, self).clean()
        cleaned_data['page'] = cleaned_data['page'] if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data


    def __process__(self):
        return Business.get_followers(
            self.author,
            self.cleaned_data['criteria'],
            self.items_per_page,
            self.cleaned_data.get('page', 0)
        )


class CoreSearchArticlesForm(IdeiaForm):

    criteria = forms.CharField(required=False)
    status = forms.ChoiceField(required=False, choices=Article.STATUS_CHOICES)
    page = forms.IntegerField(required=False)

    def __init__(self, author=None, items_per_page=10, *args, **kwargs):
        self.items_per_page = items_per_page
        self.author = author

        super(CoreSearchArticlesForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CoreSearchArticlesForm, self).clean()

        cleaned_data['page'] = cleaned_data['page'] \
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):
        return Business.get_articles(
            self.author,
            self.cleaned_data.get('criteria'),
            self.cleaned_data.get('status'),
            self.items_per_page,
            self.cleaned_data.get('page', 1)
        )


class CoreSearchVideosForm(IdeiaForm):

    criteria = forms.CharField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, author=None, items_per_page=10, *args, **kwargs):
        self.author = author
        self.items_per_page = items_per_page

        super(CoreSearchVideosForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CoreSearchVideosForm, self).clean()

        cleaned_data['page'] = cleaned_data['page'] \
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):
        return Business.get_articles_with_videos(
            self.author,
            self.cleaned_data.get('criteria'),
            self.items_per_page,
            self.cleaned_data.get('page', 1)
        )