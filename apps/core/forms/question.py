from django.db import transaction

from apps.question.service.forms import CreateQuestionForm, EditQuestionForm
from ..business import feed as CoreFeedBusiness
from taxonomies import CoreTaxonomiesMixin


class BaseCoreQuestionForm(CoreTaxonomiesMixin):

    @transaction.atomic()
    def __process__(self):
        process_question = super(BaseCoreQuestionForm, self).__process__()
        process_feed = CoreFeedBusiness.save_feed_question(self.instance, self.cleaned_data)
        process_taxonomies = self.save_taxonomies(process_feed, self.cleaned_data)
        return process_question if (process_question and process_taxonomies) else False


class CoreCreateQuestionForm(BaseCoreQuestionForm, CreateQuestionForm):

    def set_author(self, user):
        super(CoreCreateQuestionForm, self).set_author(user)
        self.filter_comunities(user)

    @transaction.atomic()
    def __process__(self):
        process_question = super(CoreCreateQuestionForm, self).__process__()
        process_feed = CoreFeedBusiness.save_feed_question(self.instance, self.cleaned_data)
        process_taxonomies = self.save_taxonomies(process_feed, self.cleaned_data)
        return process_question if (process_question and process_taxonomies) else False


class CoreEditQuestionForm(BaseCoreQuestionForm, EditQuestionForm):

    def set_author(self, user):
        super(CoreEditQuestionForm, self).set_author(user)
        self.filter_comunities(user)

    def __process__(self):
        return super(CoreEditQuestionForm, self).__process__()
