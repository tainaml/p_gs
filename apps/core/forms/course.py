from apps.custom_base.service.custom import IdeiaForm, forms
from apps.core.business import course as course_business
from apps.taxonomy.models import Taxonomy
from django.utils.translation import ugettext_lazy as _
from urllib import urlencode

class CategorylChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.description

class CommunityTaxonomylChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.description

class CourseListForm(IdeiaForm):

    CHOICES_TAXONOMY = Taxonomy.objects.filter(term__slug='categoria')

    CHOICES_ORDER_BY = (
        ('', _('Default')),
        ('-updatein', _('Recent')),
        ('updatein', _('Oldest')),
        ('-rating', _('Better rating')),
        ('rating', _('Worst rating'))
    )

    title = forms.CharField(required=False, max_length=255)
    category = CategorylChoiceField(required=False, queryset=CHOICES_TAXONOMY, empty_label=_("Category"), to_field_name="slug")

    community = CommunityTaxonomylChoiceField(required=False, queryset=Taxonomy.objects.none(), to_field_name="slug", empty_label=_("Community"))
    order = forms.ChoiceField(required=False, choices=CHOICES_ORDER_BY)
    page = forms.IntegerField(min_value=1, required=False)



    @property
    def querystring(self):
        querystring_dict = {}
        for key in self.cleaned_data:
            querystring_dict[key] = unicode(self.cleaned_data[key] or '').encode('utf-8')

        taxonomy = self.cleaned_data.get("category", None)
        if taxonomy:
            querystring_dict['category'] = taxonomy.slug

        community = self.cleaned_data.get("community", None)
        if community:
            querystring_dict['community'] = community.slug


        return urlencode(querystring_dict)


    def __init__(self, itens_per_page=10, *args, **kwargs):
        self.itens_per_page = itens_per_page
        category =  kwargs.get('data', {}).get('category', "")
        if category:
            self.declared_fields['community'].queryset = Taxonomy.objects.filter(parent__slug=category, community_related__isnull=False)
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






