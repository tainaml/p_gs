from django.contrib import admin
from apps.core.models.languages import Language


class CoreLanguageAdmin(admin.ModelAdmin):

    pass


admin.site.register(Language, CoreLanguageAdmin)