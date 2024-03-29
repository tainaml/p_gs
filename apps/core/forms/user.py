# coding=utf-8
from django.contrib.auth.forms import UserChangeForm
from django.db import transaction
from django.db.models import Q
from apps.core.business.content_types import ContentTypeCached
from apps.feed.models import ProfileStatus, FeedObject
from apps.socialactions.models import UserAction
from apps.article.models import Article
from apps.userprofile.models import Responsibility
from apps.geography.models import State, City
from apps.userprofile.service import business as BusinessUserProfile
from apps.userprofile.service.forms import EditProfileForm
from apps.socialactions.service import business as BusinessSocialActions
from apps.core.business import socialactions as CoreBusinessSocialActions
from apps.taxonomy.models import Taxonomy, Term
from ..business import user as Business
from apps.custom_base.service.custom import forms, IdeiaModelForm, IdeiaForm
from rede_gsti import settings
from django.utils.translation import ugettext as _


class CoreUserAdminForm(UserChangeForm):
    pass


class FeedForm(IdeiaModelForm):

    class Meta:
        model = ProfileStatus
        fields = ('text', 'author',)

        labels = {
            'text': _("What do you want to share with your followers?")

        }

    @transaction.atomic()
    def save(self, commit=True):
        instance = super(FeedForm, self).save(commit)
        feed = FeedObject(
            content_type=ContentTypeCached.objects.get(model='profilestatus'),
            object_id=instance.id,
            date=instance.publishin

        )
        feed.save()

class CoreUserSearchForm(IdeiaForm):

    criterio = forms.CharField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, profile_instance=None, content_types=None,
        itens_by_page=None, user=None, *args, **kwargs):

        self.profile_instance = profile_instance
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


class CoreUserMyQuestionsForm(CoreUserSearchForm):

    def __process__(self):
        return Business.get_questions_from_user(
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
        process_occupation = BusinessUserProfile.update_or_create_occupation(
            process_profile,
            responsibilities=[self.cleaned_data.get('responsibility')])

        return process_profile if (process_profile and process_occupation) else False


class CoreUserProfileEditStepOne(CoreUserProfileEditForm):



    @transaction.atomic()
    def __process__(self):
        process_profile = super(CoreUserProfileEditStepOne, self).__process__()
        if process_profile:
            BusinessUserProfile.update_wizard_step(process_profile, 1)

        return process_profile if process_profile else False


class CoreUserProfileFullEditForm(EditProfileForm):

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    responsibility = forms.ModelMultipleChoiceField(queryset=Responsibility.objects.all().order_by('name'))
    state = forms.ModelChoiceField(queryset=State.objects.filter(country=1))
    state_hometown = forms.ModelChoiceField(queryset=State.objects.filter(country=1))
    city_hometown = forms.ModelChoiceField(queryset='')

    def __init__(self, user=None, data_model=None, *args, **kwargs):
        super(CoreUserProfileFullEditForm, self).__init__(user, data_model, *args, **kwargs)

        if self.data and 'state_hometown' in self.data:
            self.fields['city_hometown'].queryset = City.objects.filter(state=self.data['state_hometown'])

    def is_valid(self):
        is_valid = super(CoreUserProfileFullEditForm, self).is_valid()
        return is_valid

    @transaction.atomic()
    def __process__(self):
        process_profile = super(CoreUserProfileFullEditForm, self).__process__()
        process_user = BusinessUserProfile.update_user(self.user, data={
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name']
        })
        process_occupation = BusinessUserProfile.update_or_create_occupation(profile=process_profile, responsibilities=self.cleaned_data.get('responsibility'))

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

        return self.author.followers_list(
            Q(author__first_name__icontains=self.cleaned_data['criteria']) |
            Q(author__last_name__icontains=self.cleaned_data['criteria']),
            self.items_per_page, self.cleaned_data['page']
        )


class CoreSearchArticlesForm(IdeiaForm):

    criteria = forms.CharField(required=False)
    status = forms.ChoiceField(required=False, choices=Article.STATUS_CHOICES)
    page = forms.IntegerField(required=False)

    def __init__(self, author=None, items_per_page=10, order=None, *args, **kwargs):
        self.items_per_page = items_per_page
        self.author = author
        self.order = order

        super(CoreSearchArticlesForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CoreSearchArticlesForm, self).clean()

        cleaned_data['page'] = cleaned_data['page'] \
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):
        return Business.get_feed_articles(
            self.author,
            self.cleaned_data.get('criteria'),
            self.cleaned_data.get('status'),
            self.items_per_page,
            self.cleaned_data.get('page', 1),
        )


class CoreSearchQuestionsForm(IdeiaForm):

    criteria = forms.CharField(required=False)
    deleted = forms.NullBooleanField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, author=None, items_per_page=10, *args, **kwargs):
        self.items_per_page = items_per_page
        self.author = author

        super(CoreSearchQuestionsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CoreSearchQuestionsForm, self).clean()

        cleaned_data['page'] = cleaned_data['page'] \
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):
        return Business.get_questions(
            self.author,
            self.cleaned_data.get('criteria'),
            self.cleaned_data.get('deleted'),
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


class CoreSearchCommunitiesForm(IdeiaForm):

    criteria = forms.CharField(required=False)
    __term = None
    try:
        __term = Term.objects.get(description__icontains='categoria')
    except:
        pass
    category = forms.ModelChoiceField(queryset=Taxonomy.objects.filter(term=__term), required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, author, items_per_page, *args, **kwargs):
        self.author = author
        self.items_per_page = items_per_page

        super(CoreSearchCommunitiesForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CoreSearchCommunitiesForm, self).clean()

        cleaned_data['page'] = cleaned_data['page'] \
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):
        return BusinessSocialActions.get_users_acted_by_author_with_parameters(
            author=self.author,
            action=settings.SOCIAL_FOLLOW,
            content_type='community',
            items_per_page=self.items_per_page,
            page=self.cleaned_data.get('page', 1),
            criteria=self.cleaned_data.get('criteria'),
            category=self.cleaned_data.get('category')
        )


class CoreSearchFavouriteForm(IdeiaForm):

    criteria = forms.CharField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, author, items_per_page, *args, **kwargs):

        self.author = author
        self.items_per_page = items_per_page

        super(CoreSearchFavouriteForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CoreSearchFavouriteForm, self).clean()

        cleaned_data['page'] = cleaned_data['page'] \
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def __process__(self):
        return CoreBusinessSocialActions.get_favourite_content(
            self.author,
            self.cleaned_data.get('criteria'),
            self.items_per_page,
            self.cleaned_data.get('page', 1)
        )


class CoreRemoveSocialActionForm(IdeiaForm):

    items_to_remove = forms.ModelMultipleChoiceField(queryset=UserAction.objects.all())

    def __init__(self, action, *args, **kwargs):

        self.action = action
        self.processed = False
        self.author = None
        self.target_user = None

        super(CoreRemoveSocialActionForm, self).__init__(*args, **kwargs)

    def is_valid(self):

        is_valid = super(CoreRemoveSocialActionForm, self).is_valid()

        action_allowed = [settings.SOCIAL_SUGGEST, settings.SOCIAL_FAVOURITE, settings.SOCIAL_SEE_LATER]

        if self.action not in action_allowed:
            is_valid = False

        return is_valid

    def set_author(self, author):
        self.author = author

    def set_target_user(self, user):
        self.target_user = user

    def __process__(self):

        self.processed = CoreBusinessSocialActions.remove_social_actions(
            self.action,
            self.cleaned_data.get('items_to_remove'),
            self.author,
            self.target_user
        )

        return self.processed


class CoreSearchSocialActionsForm(IdeiaForm):
    criteria = forms.CharField(required=False)
    page = forms.IntegerField(required=False)

    def __init__(self, action, items_per_page, *args, **kwargs):

        self.action = action
        self.items_per_page = items_per_page
        self.author = None
        self.target_user = None

        super(CoreSearchSocialActionsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CoreSearchSocialActionsForm, self).clean()

        cleaned_data['page'] = cleaned_data['page'] \
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def is_valid(self):

        is_valid = super(CoreSearchSocialActionsForm, self).is_valid()

        action_allowed = [settings.SOCIAL_SUGGEST, settings.SOCIAL_FAVOURITE, settings.SOCIAL_SEE_LATER]

        if self.action not in action_allowed:
            is_valid = False

        return is_valid

    def set_author(self, author):
        self.author = author

    def set_target_user(self, user):
        self.target_user = user

    def __process__(self):
        return CoreBusinessSocialActions.get_content_by_action(
            self.cleaned_data.get('criteria'),
            self.action,
            self.items_per_page,
            self.cleaned_data.get('page', 1),
            self.author,
            self.target_user
        )
