from apps.article.models import Article
from apps.core.admin.geral import FeedInline
from django.contrib import admin
from django import forms
from ideia_summernote.widget import SummernoteWidget
from reversion.admin import VersionAdmin


class ArticleAdminForm(forms.ModelForm):

    class Media:
        js = (
            'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.1/summernote.min.js', )

        css= {
            'all': (
                'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
                'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.1/summernote.css',
            )
        }

    class Meta:
        excludes = ()
        widgets = {
            'text': SummernoteWidget(editor_conf='article_admin'),
            # 'author': SelectizeSelectSingle(
            #     unique_name='admin_authors',
            #     label_field='username',
            #     search_fields=(
            #         'username__unaccent__icontains',
            #         'first_name__unaccent__icontains',
            #         'last_name__unaccent__icontains',
            #     )
            # ),
        }


class ArticlelAdmin(VersionAdmin):

    form = ArticleAdminForm

    list_display = ('id', 'title', 'slug', 'status', 'publishin', 'show_author_name')
    search_fields = ('id', 'title', 'slug')
    list_display_links = ('id', 'title', 'slug')

    list_filter = ['status']

    inlines = [FeedInline]

    def show_author_name(self, obj):
        return obj.author.get_full_name()
    show_author_name.short_description = 'Author'


admin.site.register(Article, ArticlelAdmin)