from apps.custom_base.service.custom import IdeiaForm, forms
from apps.core.business import course as course_business
from apps.taxonomy.models import Taxonomy
from django.utils.translation import ugettext_lazy as _


class CourseListForm(IdeiaForm):

    CHOICES_TAXONOMY = Taxonomy.objects.filter(term__slug='categoria')

    CHOICES_ORDER_BY = (
        ('', _('Default')),
        ('updatein', _('Recent')),
        ('-updatein', _('Oldest')),
        ('rating', _('Rating')),
        ('-rating', _('Rating'))
    )

    category = forms.ChoiceField(required=False, choices=CHOICES_TAXONOMY)
    community = forms.ChoiceField(required=False, choices=('',))
    order = forms.ChoiceField(required=False, choices=CHOICES_ORDER_BY)
    page = forms.IntegerField(min_value=1, required=False)

    def __init__(self, itens_per_page=10, *args, **kwargs):
        self.itens_per_page = itens_per_page
        super(CourseListForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CourseListForm, self).clean()
        cleaned_data['page'] = cleaned_data['page']\
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def is_valid(self):
        valid = super(CourseListForm, self).is_valid()

        return valid

    def __process__(self):

        return  course_business.get_courses(self.itens_per_page, **self.cleaned_data)




