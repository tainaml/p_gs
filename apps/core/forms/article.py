from django.core.exceptions import ValidationError
from apps.article.service.forms import ArticleForm, IdeiaModelForm
from apps.taxonomy.models import ObjectTaxonomy

class CoreArticleCategoriesForm(IdeiaModelForm):

    class Meta:
        model = ObjectTaxonomy
        exclude = []


    def is_valid(self):
        valid = super(CoreArticleCategoriesForm, self).is_valid()

        return valid


class CoreArticleForm(ArticleForm):

    def is_valid(self):

        valid = super(CoreArticleForm, self).is_valid()
        print 'data'
        print self.data
        #tax_instance = ObjectTaxonomy.objects.get(object_id=self.cleaned_data['id'])
        #tax_form = CoreArticleCategoriesForm(self.data, prefix='categoria', instance=tax_instance)

        return valid