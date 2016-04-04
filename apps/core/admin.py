from django.contrib import admin
from django.utils.translation import ugettext as _

# Register your models here.
from reversion_compare.admin import CompareVersionAdmin
from apps.article.models import Article
from apps.core.models.tags import Tags
from apps.question.models import Question
from apps.account.admin import UserAdmin, User
from apps.userprofile.models import UserProfile

admin.site.register(Tags)
admin.site.unregister(User)


class ArticlelAdmin(CompareVersionAdmin):
    pass


class QuestionAdmin(CompareVersionAdmin):
    pass


class CoreProfile(admin.StackedInline):
    model = UserProfile
    verbose_name = _("Profile")
    verbose_name_plural = _("Profiles")


class CoreUserAdmin(UserAdmin):

    inlines = [
        CoreProfile
    ]


admin.site.register(Article, ArticlelAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(User, CoreUserAdmin)
