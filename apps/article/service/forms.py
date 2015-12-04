from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils import timezone
from custom_forms.custom import forms, IdeiaModelForm
from django.utils.translation import ugettext as _
import business as Business
from rede_gsti import settings


class ArticleForm(IdeiaModelForm):

    title = forms.CharField(required=True, max_length=100)
    slug = forms.SlugField(max_length=150, required=False)
    text = forms.CharField(required=True, min_length=200, max_length=2048, widget=CKEditorWidget(config_name='article'))
    image = forms.ImageField(required=False)
    publishin = forms.DateTimeField(required=False)
    status = forms.ChoiceField(required=False, choices=Business.Article.STATUS_CHOICES)
    author = forms.IntegerField(required=False)

    # Actions: save, publish, schedule
    ACTION_SAVE = 1
    ACTION_PUBLISH = 2
    ACTION_SCHEDULE = 3

    action = ACTION_SAVE

    class Meta:
        model = Business.Article
        exclude = []

    def __init__(self, data=None, files=None, author=False, *args, **kwargs):

        super(ArticleForm, self).__init__(data, files, *args, **kwargs)

        if author:
            self.set_author(author)


    def clean_publishin(self):
        _date = self.cleaned_data.get('publishin')
        _now = timezone.now()

        if self.action == self.ACTION_SCHEDULE:
            if not _date:
                self.add_error('publishin', ValidationError(_('Publish date has invalid')))
            elif _date < _now:
                self.add_error('publishin', ValidationError(_('Publish date has invalid')))
            else:
                _date = _date if _date else _now
                
        elif self.action == self.ACTION_PUBLISH:
            _date = timezone.now()

        return _date

    def clean_status(self):
        _status = self.cleaned_data.get('status',
                                        Business.Article.STATUS_DRAFT)
        if self.action in [self.ACTION_PUBLISH, self.ACTION_SCHEDULE]:
            _status = Business.Article.STATUS_PUBLISH

        return _status

    def clean_slug(self):
        _slug = self.cleaned_data.get('slug', '')
        _title = self.cleaned_data.get('title')
        _slug = _slug if _slug else slugify(_title)
        return _slug

    def clean_author(self):
        _author = self.cleaned_data.get('author')
        return _author if _author else self._author

    def is_valid(self):
        valid = True

        if not super(ArticleForm, self).is_valid():
            valid = False

        image = self.cleaned_data.get('image', False)

        if image:
            if image.content_type not in settings.IMAGES_ALLOWED:
                self.add_error('image',
                               ValidationError(_('Image format is not allowed.'), code='image'))
                valid = False

        if 'submit-publish' in self.data:
            '''
            Publishing action
            '''
            self.action = self.ACTION_PUBLISH

        elif 'submit-schedule' in self.data:
            self.__action = self.ACTION_SCHEDULE

        elif 'submit-save' in self.data:
            self.action = self.ACTION_SAVE

        #if 'submit-schedule' in self.data:
        return valid

    def set_author(self, author):
        self._author = author

    def __process__(self):
        return Business.save_article(self.instance, self.cleaned_data)