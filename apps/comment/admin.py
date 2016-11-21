from django.contrib import admin

from apps.comment.models import Comment

class CommentAdmin(admin.ModelAdmin):

    raw_id_fields = ('author',)

admin.site.register(Comment, CommentAdmin)