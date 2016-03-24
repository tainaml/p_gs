# Register your models here.

from django.contrib import admin
from django.core.urlresolvers import reverse


from .models import FeedObject


class FeedObjectAdmin(admin.ModelAdmin):
    exclude = ('content_type', 'object_id', )
    list_display = ('content_object', )
    def view_on_site(self, obj):

        if obj.content_type.model == "article":
            return reverse('article:view', args=[obj.content_object.id, obj.content_object.slug])
        elif obj.content_type.model == "question":
            return reverse('question:show', args=[obj.content_object.slug, obj.content_object.id])


admin.site.register(FeedObject, FeedObjectAdmin)