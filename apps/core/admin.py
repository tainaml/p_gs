from django.contrib import admin
from django.utils.translation import ugettext as _

# Register your models here.
from reversion_compare.admin import CompareVersionAdmin
from apps.article.models import Article
from apps.core.models.tags import Tags
from apps.question.models import Question
from apps.account.admin import UserAdmin, User
from apps.userprofile.models import UserProfile
from ckeditor_uploader.widgets import CKEditorUploadingWidget
admin.site.register(Tags)
admin.site.unregister(User)


class ArticlelAdmin(CompareVersionAdmin):
    list_display = ('id', 'title',)
    search_fields = ['id', 'title']
    class Meta:
        widgets = {'text': CKEditorUploadingWidget(config_name='article')}
        excludes = ()

class QuestionAdmin(CompareVersionAdmin):
    pass


class CoreProfile(admin.StackedInline):
    model = UserProfile
    verbose_name = _("Profile")
    verbose_name_plural = _("Profiles")


class CoreUserAdmin(UserAdmin):

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


admin.site.register(Article, ArticlelAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(User, CoreUserAdmin)
