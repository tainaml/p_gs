# Register your models here.

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.core.urlresolvers import reverse
from apps.article.models import Article

from .models import FeedObject



class FeedObjectAdmin(admin.ModelAdmin):
    exclude = ('content_type', 'object_id', )
    list_display = ('content_object', 'show_content_type')
    search_fields = ['article__title', 'question__title']

    list_filter = [
        ('content_type', admin.RelatedOnlyFieldListFilter)
    ]

    def show_content_type(self, obj):
        return obj.content_type
    show_content_type.short_description = 'Content Type'

    def view_on_site(self, obj):

        if obj.content_type.model == "article":
            return reverse('article:view', args=[obj.content_object.year, obj.content_object.month, obj.content_object.slug])
        elif obj.content_type.model == "question":
            return reverse('question:show', args=[obj.content_object.slug, obj.content_object.id])


admin.site.register(FeedObject, FeedObjectAdmin)