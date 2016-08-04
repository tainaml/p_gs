from django.contrib import admin
from django_thumbor import generate_url
from .models import Community
from django.conf import settings
from django import forms


class ComunnityAdminForm(forms.ModelForm):
    class Meta:
        excludes = ()


class CommunityAdmin(admin.ModelAdmin):

    form = ComunnityAdminForm

    list_display = ('resized_image', 'title', 'slug', 'category')
    filter_horizontal = ['related']
    ordering = ['title']

    list_display_links = ('resized_image', 'title', 'slug')
    search_fields = ['title', 'slug']

    def category(self, obj):
        return obj.taxonomy.parent

    def resized_image(self, obj):
        if obj.image and obj.image.url:
            url = generate_url(obj.image.url, thumbor_server=settings.THUMBOR_SERVER, width=30)
            img = "<img src=\"%s\" />" % url
            return img
        else:
            return "No image"

    resized_image.allow_tags = True

admin.site.register(Community, CommunityAdmin)
