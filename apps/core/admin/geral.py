from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Q
from django.utils.translation import ugettext as _

# Register your models here.
from reversion.admin import VersionAdmin
from apps.article.models import Article
from apps.core.forms.user import CoreUserAdminForm
from apps.core.models.tags import Tags
from apps.feed.models import FeedObject
from apps.question.models import Question
from apps.account.admin import User, UserNewAdmin
from apps.socialactions.models import UserAction
from apps.userprofile.models import UserProfile
from django import forms
from ideia_summernote.widget import SummernoteWidget
from django.contrib.humanize.templatetags.humanize import naturaltime

admin.site.register(Tags)
admin.site.unregister(User)


class CoreProfile(admin.StackedInline):
    model = UserProfile__author__ = 'jroque'

    verbose_name = _("Profile")
    verbose_name_plural = _("Profiles")


class WizardFilter(SimpleListFilter):
    title = "Passo no Wizard"
    parameter_name = 'step'
    # Set the displaying options
    def lookups(self, request, model_admin):
        return (
            (0, "Nao iniciou wizard"),
            (1, "Passo 1"),
            (2, "Passo 2"),
            (3, "Passo 3"),
        )
    # Assign a query for each option
    def queryset(self, request, queryset):

        step = self.value()
        if step:
            return queryset.filter(profile__wizard_step=step)

class SocialFilter(SimpleListFilter):
    title = "Tipo de Cadastro"
    parameter_name = 'social'
    # Set the displaying options
    def lookups(self, request, model_admin):
        return (
            ('false', "Cadastro padrao"),
            ('true', "Redes sociais"),
            ('facebook', "Facebook"),
            ('google-oauth2', "Google+"),
            ('linkedin', "Linkedin"),
        )
    SOCIAL_PROVIDERS = [
        'facebook',
        'google-oauth2',
        'linkedin'
    ]

    def queryset(self, request, queryset):

        social_filter = self.value()
        print social_filter

        if social_filter == 'false':
            return queryset.filter(social_auth__isnull=True)
        elif social_filter == 'true':
            return queryset.filter(social_auth__isnull=False)
        elif social_filter in self.SOCIAL_PROVIDERS:
            return queryset.filter(social_auth__provider=social_filter)


class CoreUserAdmin(UserNewAdmin):

    form = CoreUserAdminForm
    list_filter = ('is_active', 'profile__contributor', WizardFilter, SocialFilter)
    list_display = [
        'username', 'show_full_name',
        'show_staff', 'is_active', 'show_contributor', 'show_wizard_is_complete',
        'date_joined', 'show_login'
    ]

    list_display_links = [
        'username', 'show_full_name'
    ]

    def wizard(self, obj):
        return User.objects.filter(profile__wizard=3)

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
    #
    # show_date_joined.admin_order_field = 'date_joined'
    # show_date_joined.short_description = 'Criado em'

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

class QuestionAdmin(VersionAdmin):
    raw_id_fields = ('author',)

    inlines = [FeedInline]


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

    raw_id_fields = ('author',)
    list_filter = ['status']


    inlines = [FeedInline]

    def show_author_name(self, obj):
        return obj.author.get_full_name()
    show_author_name.short_description = 'Author'


admin.site.register(UserAction)
admin.site.register(Question, QuestionAdmin)
admin.site.register(User, CoreUserAdmin)
