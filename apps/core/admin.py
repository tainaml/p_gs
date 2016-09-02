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

    list_display = UserAdmin.list_display + ('show_contributor',)

    inlines = [
        CoreProfile
    ]

    def show_contributor(self, obj):
        return obj.profile.contributor

    show_contributor.short_description = _("Contributor")
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


class ArticlelAdmin(CompareVersionAdmin):

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
