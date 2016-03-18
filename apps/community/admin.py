from django.contrib import admin

from .models import Community


class CommunityAdmin(admin.ModelAdmin):
    filter_horizontal = ['related']
    ordering = ['title']
    search_fields = ['title']

admin.site.register(Community, CommunityAdmin)
