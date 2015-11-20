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
from taxonomies import CoreTaxonomiesMixin


class BaseCoreQuestionForm(CoreTaxonomiesMixin):

    @transaction.atomic()
    def __process__(self):
        process_question = super(BaseCoreQuestionForm, self).__process__()
        process_feed = CoreFeedBusiness.save_feed_question(self.instance, self.cleaned_data)
        process_taxonomies = self.save_taxonomies(process_feed, self.cleaned_data)

        return process_question if (process_question and process_taxonomies) else False


class CoreCreateQuestionForm(CreateQuestionForm, BaseCoreQuestionForm):

    def set_author(self, user):
        super(CoreCreateQuestionForm, self).set_author(user)
        self.filter_comunities(user)


class CoreEditQuestionForm(EditQuestionForm, BaseCoreQuestionForm):

    def set_author(self, user):
        super(CoreEditQuestionForm, self).set_author(user)
        self.filter_comunities(user)

