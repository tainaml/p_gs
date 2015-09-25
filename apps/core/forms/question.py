from django.core.exceptions import ValidationError
from django.db import transaction
from apps.question.service.forms import CreateQuestionForm, forms
from apps.taxonomy.models import Taxonomy
from ..business import question as Business


class CoreCreateQuestionForm(CreateQuestionForm):

    taxonomies = forms.ModelMultipleChoiceField(queryset=Taxonomy.objects.all())

    @transaction.atomic()
    def __process__(self):
        process_question = super(CoreCreateQuestionForm, self).__process__()
        process_feed = Business.save_feed_item(self.instance, self.cleaned_data)
        process_core = Business.save_taxonomies(process_feed, self.cleaned_data)

        return process_question if (process_question and process_core) else False
