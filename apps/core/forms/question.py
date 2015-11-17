from django.db import transaction
from apps.community.models import Community
from apps.question.views import SaveQuestionView
from apps.taxonomy.models import Taxonomy
from apps.feed.service import business as FeedBusiness
from apps.taxonomy.service import business as TaxonomyBusiness
from apps.question.service.forms import forms,\
    IdeiaForm, IdeiaModelForm, \
    CreateQuestionForm, EditQuestionForm
from ..business import user as UserBusiness
from ..business import feed as CoreFeedBusiness


class CoreQuestionMixinForm(IdeiaModelForm):

    taxonomies = forms.ModelMultipleChoiceField(required=False, queryset=Taxonomy.objects.all(),)
    communities = forms.ModelMultipleChoiceField(required=True, queryset=Community.objects.all(),)

    def __init__(self, *args, **kwargs):

        kwargs['initial'] = kwargs.get('initial', {})
        instance = kwargs.get('instance', None)

        if instance is not None:
            feed_item = FeedBusiness.feed_get_or_create(instance)

            initial = {
                'communities': feed_item.communities.all(),
                'taxonomies': feed_item.taxonomies.all()
            }

            kwargs['initial'].update(initial)

        super(CoreQuestionMixinForm, self).__init__(*args, **kwargs)

        communities = self.fields.get('communities')
        if communities:
            communities.queryset = UserBusiness.get_user_communities(self.user)


    def __process__(self):
        process_question = super(CoreQuestionMixinForm, self).__process__()
        process_feed = FeedBusiness.save_feed_item(process_question)

        process_communities = CoreFeedBusiness.save_communities(process_feed, self.cleaned_data)
        process_core = CoreFeedBusiness.save_taxonomies(process_feed, self.cleaned_data)

        return process_question if (process_question and process_communities and process_core) else False


class CoreCreateQuestionForm(CreateQuestionForm, CoreQuestionMixinForm):

    def __init__(self, user=None, *args, **kargs):
        self.user = user
        super(CoreCreateQuestionForm, self).__init__(*args, **kargs)


class CoreEditQuestionForm(EditQuestionForm, CoreQuestionMixinForm):

    def __process__(self):
        return super(CoreEditQuestionForm, self).__process__()
