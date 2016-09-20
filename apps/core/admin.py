from datetime import date
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import ugettext as _

# Register your models here.
from reversion.admin import VersionAdmin
from apps.article.models import Article
from apps.core.forms.user import CoreUserAdminForm
from apps.core.models.tags import Tags
from apps.feed.models import FeedObject
from apps.question.models import Question
from apps.account.admin import UserAdmin, User, UserNewAdmin
from apps.socialactions.models import UserAction
from apps.userprofile.models import UserProfile
from django import forms
from ideia_summernote.widget import SummernoteWidget
from django.contrib.humanize.templatetags.humanize import naturaltime

admin.site.register(Tags)
admin.site.unregister(User)




class QuestionAdmin(VersionAdmin):
    pass


class CoreProfile(admin.StackedInline):
    model = UserProfile
    verbose_name = _("Profile")
    verbose_name_plural = _("Profiles")


class CoreUserAdmin(UserNewAdmin):

    form = CoreUserAdminForm

    list_display = [
        'username', 'show_full_name',
        'show_staff', 'is_active', 'show_contributor', 'show_wizard_is_complete',
        'show_date_joined', 'show_login'
    ]

    list_display_links = [
        'username', 'show_full_name'
    ]

    inlines = [
        CoreProfile
    ]

    def show_full_name(self, obj):
        return u"{name} {last_name}".format(
            name=obj.first_name,
            last_name=obj.last_name
        )

    def show_contributor(self, obj):
        return obj.profile.contributor

    def show_staff(self, obj):
        return obj.is_staff

    def show_wizard_is_complete(self, obj):

        try:
            return obj.profile.has_wizard_completed()
        except Exception:
            return False

    def show_date_joined(self, obj):
        try:
            return obj.date_joined.strftime('%d/%m/%Y %H:%M')
        except Exception:
            return "-"

    def show_login(self, obj):
        return naturaltime(obj.last_login)

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if isinstance(inline, CoreProfile) and obj is None:
                continue
            yield inline.get_formset(request, obj), inline


    show_full_name.short_description = _("Name")

    show_contributor.short_description = _("Contributor")

    show_staff.short_description = 'Membro'
    show_staff.boolean = True

    show_date_joined.admin_order_field = 'date_joined'
    show_date_joined.short_description = 'Criado em'

    show_login.short_description = 'Login'
    show_login.admin_order_field = 'last_login'

    show_wizard_is_complete.short_description = _('Completed Wizard?')
    show_wizard_is_complete.boolean = True

    show_contributor.boolean = True


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


admin.site.register(UserAction)
admin.site.register(Article, ArticlelAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(User, CoreUserAdmin)
