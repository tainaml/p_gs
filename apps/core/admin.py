from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import ugettext as _

# Register your models here.
from reversion_compare.admin import CompareVersionAdmin
from apps.article.models import Article
from apps.core.forms.user import CoreUserAdminForm
from apps.core.models.tags import Tags
from apps.feed.models import FeedObject
from apps.question.models import Question
from apps.account.admin import UserAdmin, User
from apps.socialactions.models import UserAction
from apps.userprofile.models import UserProfile
from django import forms
from ideia_summernote.widget import SummernoteWidget
from django.contrib.humanize.templatetags.humanize import naturaltime

admin.site.register(Tags)
admin.site.unregister(User)




class QuestionAdmin(CompareVersionAdmin):
    pass


class CoreProfile(admin.StackedInline):
    model = UserProfile
    verbose_name = _("Profile")
    verbose_name_plural = _("Profiles")


class CoreUserAdmin(UserAdmin):

    form = CoreUserAdminForm

    list_display = ('id', 'username', 'first_name', 'last_name', 'show_staff', "is_active", 'show_contributor', "show_date_joined", "show_login",)

    inlines = [
        CoreProfile
    ]

    def show_contributor(self, obj):
        return obj.profile.contributor

    show_contributor.short_description = _("Contributor")

    def show_staff(self, obj):
        return obj.is_staff


    show_staff.short_description = 'Membro'
    show_staff.boolean = True

    def show_date_joined(self, obj):

        return obj.date_joined

    show_date_joined.admin_order_field = 'date_joined'
    show_date_joined.short_description = 'Criado em'


    def show_login(self, obj):
        return naturaltime(obj.last_login)

    def show_joined(self, obj):
        return naturaltime(obj.last_login)

    show_login.short_description = 'Login'
    show_login.admin_order_field = 'last_login'

    show_contributor.boolean = True

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if isinstance(inline, CoreProfile) and obj is None:
                continue
            yield inline.get_formset(request, obj), inline


class FeedInline(GenericTabularInline):

    model = FeedObject
    extra = 0
    min_num = 1
    max_num = 1


class ArticleAdminForm(forms.ModelForm):



    class Media:
        js = (
            # 'https://code.jquery.com/jquery-2.2.4.min.js',
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
          'text': SummernoteWidget(editor_conf='article_admin')
        }


class ArticlelAdmin(CompareVersionAdmin):

    form = ArticleAdminForm

    list_display = ('id', 'title', 'slug', 'status', 'publishin', 'show_author_name')
    search_fields = ('id', 'title', 'slug')
    list_display_links = ('id', 'title', 'slug')

    list_filter = ['status']

    inlines = [FeedInline]

    def show_author_name(self, obj):
        return obj.author.get_full_name()
    show_author_name.short_description = 'Author'


admin.site.register(UserAction)
admin.site.register(Article, ArticlelAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(User, CoreUserAdmin)
