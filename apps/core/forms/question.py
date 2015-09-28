from django.db import transaction
from apps.taxonomy.models import Taxonomy
from apps.feed.service import business as FeedBusiness
from apps.taxonomy.service import business as TaxonomyBusiness
__author__ = 'phillip'
from apps.question.service.forms import CreateQuestionForm, forms

class CoreQuestionForm(CreateQuestionForm):
    taxonomies = forms.ModelMultipleChoiceField(queryset=Taxonomy.objects.all())

    @transaction.atomic
    def __process__(self):
        process_question = super(CoreQuestionForm, self).__process__()
        process_feed = FeedBusiness.save_feed_item(process_question)
        process_taxonomies = TaxonomyBusiness.save_taxonomies_for_model(process_feed, self.cleaned_data['taxonomies'])

        return process_question if (process_question and process_taxonomies) else False
