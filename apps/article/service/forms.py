from django.core.exceptions import ValidationError

from django.utils import timezone
from django.utils.translation import ugettext as _
from ideia_summernote.widget import SummernoteWidget

from apps.custom_base.service.custom import forms, IdeiaModelForm
from django.conf import settings
import business as Business
import re


class ArticleForm(IdeiaModelForm):

    title = forms.CharField(required=True, max_length=settings.ARTICLE_TITLE_LIMIT if hasattr(settings, "ARTICLE_TITLE_LIMIT") else 100)
    slug = forms.SlugField(max_length=150, required=False)
    text = forms.CharField(required=True, widget=SummernoteWidget(editor_conf='article'), max_length=settings.ARTICLE_TEXT_LIMIT if hasattr(settings, "ARTICLE_TEXT_LIMIT") else 10000)
    # image = forms.ImageField(required=False)
    publishin = forms.DateTimeField(required=False)
    # status = forms.ChoiceField(required=False, choices=Business.Article.STATUS_CHOICES)
    # author = forms.IntegerField(required=False)

    # Actions: save, publish, schedule
    ACTION_SAVE = 1
    ACTION_PUBLISH = 2
    ACTION_SCHEDULE = 3

    action = ACTION_SAVE

    _author = None

    class Meta:
        model = Business.Article
        exclude = ['first_slug', 'slug','status', 'search_vector', 'author', 'comment_count', 'like_count', 'dislike_count']

    def __init__(self, data=None, files=None, author=False, *args, **kwargs):

        super(ArticleForm, self).__init__(data, files, *args, **kwargs)

        # if author:
        #     self.set_author(author)

    def clean_text(self):
        regex = re.compile(r'<p>&nbsp;</p>')
        _text = regex.sub('', self.cleaned_data.get('text'))

        return _text

    def clean_publishin(self):
        _date = self.cleaned_data.get('publishin')
        _instance_date = self.instance.publishin
        _now = timezone.now()

        if not _date and _instance_date:
            _date = _instance_date

        if self.action == self.ACTION_SCHEDULE:
            if not _date:
                self.add_error('publishin', ValidationError(_('Publish date has invalid')))
            elif _date < _now:
                self.add_error('publishin', ValidationError(_('Publish date has invalid')))
            else:
                _date = _date if _date else _now
                
        elif self.action == self.ACTION_PUBLISH:
            _date = _now

        return _date

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', None)
        title = self.cleaned_data.get('title')
        slug = slug if bool(slug) else Business.get_valid_slug(self.instance, title)
        return slug

    # def clean_author(self):
    #     _author = self.cleaned_data.get('author')
    #     return _author if _author else self._author

    def is_valid(self):
        valid = True

        old_status_is_published = False

        if not super(ArticleForm, self).is_valid():
            valid = False

        if self.instance.status == Business.Article.STATUS_PUBLISH:
            old_status_is_published = Business.Article.STATUS_PUBLISH

        slug = self.cleaned_data.get('slug', None)
        if bool(slug) and self.is_author():
            title = self.cleaned_data.get('title')
            slug = slug if bool(slug) else Business.get_valid_slug(self.instance, title)
            self.instance.slug = slug

        if bool(self.instance.slug) and not self.is_author():
            self.cleaned_data.pop('slug')

        image = self.cleaned_data.get('image', False)

        if image and 'image' in self.changed_data:
            if image.content_type not in settings.IMAGES_ALLOWED:
                self.add_error('image',
                               ValidationError(_('Image format is not allowed.'), code='image_format_incorrect'))
                valid = False

        if image and 'image' in self.changed_data:
            if image.size > 2621440: #2,5 MB
                self.add_error('image',
                               ValidationError(_('Image size is too long.'), code='image_size_soo_long'))
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

            if self.instance.status == Business.Article.STATUS_TEMP:
                self.instance.status = Business.Article.STATUS_DRAFT

            self.instance.do_save()

        # self.cleaned_data.update({
        #     'status': self.instance.status
        # })

        if old_status_is_published and 'publishin' in self.cleaned_data:
            del self.cleaned_data['publishin']

        return valid

    def is_author(self):
        return bool(self.instance.author == self._author)

    def set_author(self, author):
        self._author = author

    def __process__(self):
        if not self.instance.author:
            self.instance.author = self._author

        self.instance = self.save()
        return Business.save_article(self.instance, self.cleaned_data)
