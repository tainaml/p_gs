from dbus.service import FallbackObject
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Model
import business as Business
from custom_forms.custom import forms, IdeiaForm
from django.utils.translation import ugettext as _
from django.forms import model_to_dict, ModelForm
from ..models import Article


class ArticleForm(ModelForm):
    pass



class ArticleFormB(IdeiaForm):

    title = forms.CharField(required=True, max_length=100)
    slug = forms.SlugField(max_length=150)
    text = forms.CharField(required=True, min_length=200, max_length=2048)
    image = forms.ImageField()
    publishin = forms.DateTimeField(required=False)
    status = forms.ChoiceField(required=True, choices=Article.STATUS_CHOICES)

    def __init__(self, data=None, files=None, data_model=None, *args, **kwargs):
        super(ArticleForm, self).__init__(data, files, *args, **kwargs)
        if data_model and isinstance(data_model, Model):
            self.data.update(forms.model_to_dict(data_model))

    def is_valid(self):
        return True

    def __process__(self):
        return True