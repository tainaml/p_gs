from django.contrib import admin

# Register your models here.
from reversion_compare.admin import CompareVersionAdmin
from apps.article.models import Article
from apps.core.models.tags import Tags
from apps.question.models import Question

admin.site.register(Tags)

class ArticlelAdmin(CompareVersionAdmin):
    pass

class QuestionAdmin(CompareVersionAdmin):
    pass


admin.site.register(Article, ArticlelAdmin)
admin.site.register(Question, QuestionAdmin)
