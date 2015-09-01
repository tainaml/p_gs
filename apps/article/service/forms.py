from django.forms import ModelForm, model_to_dict
from django.template.defaultfilters import slugify
from custom_forms.custom import forms, IdeiaForm
import business as Business

class IdeiaModelForm(ModelForm):
    def process(self):
        try:
            return self.__process__() if self.is_valid() else False
        except NotImplementedError:
            raise NotImplementedError
        except Exception, e:
            print e.message
            self.add_error(None, "General error!")
            return False

    def __process__(self):
        raise NotImplementedError


class ArticleForm(IdeiaModelForm):

    title = forms.CharField(required=True, max_length=100)
    slug = forms.SlugField(max_length=150, required=False)
    text = forms.CharField(required=True, min_length=200, max_length=2048, widget=forms.Textarea)
    image = forms.ImageField(required=False)
    publishin = forms.DateTimeField(required=False)
    status = forms.ChoiceField(required=True, choices=Business.Article.STATUS_CHOICES)
    author = forms.IntegerField(required=False)

    class Meta:
        model = Business.Article
        exclude = []

    def clean_slug(self):
        _slug = self.cleaned_data.get('slug', '')
        _title = self.cleaned_data.get('title')
        _slug = _slug if _slug else slugify(_title)
        return _slug

    def clean_author(self):
        _author = self.cleaned_data.get('author')
        return _author if _author else self._author

    def set_author(self, author):
        self._author = author

    def is_valid(self):
        valid = super(ArticleForm, self).is_valid()
        return valid

    def __process__(self):
        return Business.save_article(self.instance, self.cleaned_data)