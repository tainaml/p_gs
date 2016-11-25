from django.core.exceptions import ValidationError

__author__ = 'phillip'
from apps.custom_base.service.custom import IdeiaForm, forms


class CourseListForm(IdeiaForm):

    content_id = forms.IntegerField(min_value=1, required=True)
    content_type = forms.CharField(required=True)
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

        if 'content_type' in self.cleaned_data and self.cleaned_data['content_type'] not in settings.ENTITY_TO_COMMENT:
            self.add_error(None,
                           ValidationError(('ContentType not found in comment contentType list.'),
                                           code='comment_content_type_not_found'))

        return valid

    def __process__(self):
        return  Business.get_comments_by_content_type_and_id(
            self.cleaned_data['content_type'],
            self.cleaned_data['content_id'],
            self.itens_per_page,
            self.cleaned_data['page']
        )



