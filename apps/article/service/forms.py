from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import ugettext as _

from apps.custom_base.service.custom import forms, IdeiaModelForm
from rede_gsti import settings

import business as Business
import re


class ArticleForm(IdeiaModelForm):

    title = forms.CharField(required=True, max_length=70)
    slug = forms.SlugField(max_length=150, required=False)
    text = forms.CharField(required=True, min_length=200, widget=CKEditorUploadingWidget(config_name='article'))
    image = forms.ImageField(required=False)
    publishin = forms.DateTimeField(required=False)
    status = forms.ChoiceField(required=False, choices=Business.Article.STATUS_CHOICES)
    author = forms.IntegerField(required=False)

    # Actions: save, publish, schedule
    ACTION_SAVE = 1
    ACTION_PUBLISH = 2
    ACTION_SCHEDULE = 3

    action = ACTION_SAVE

    _author = None

    class Meta:
        model = Business.Article
        exclude = []

    def __init__(self, data=None, files=None, author=False, *args, **kwargs):

        super(ArticleForm, self).__init__(data, files, *args, **kwargs)

        if author:
            self.set_author(author)

    def clean_text(self):
        regex = re.compile(r'<p>&nbsp;</p>')
        _text = regex.sub('', self.cleaned_data.get('text'))

        return _text

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

        if image and 'image' in self.changed_data:
            if image.content_type not in settings.IMAGES_ALLOWED:
                self.add_error('image',
                               ValidationError(_('Image format is not allowed.'), code='image'))
                valid = False

        if 'submit-publish' in self.data:
            '''
            Publishing action
            '''
            self.action = self.ACTION_PUBLISH
            self.instance.do_publish()

        elif 'submit-save' in self.data:
            '''
            Save action
            '''
            self.instance.action = self.ACTION_SAVE
            self.instance.do_save()

        return valid

    def set_author(self, author):
        self._author = author

    def __process__(self):
        return Business.save_article(self.instance, self.cleaned_data)