# Register your models here.
from django.contrib import admin
from django.conf import settings
from django.core.urlresolvers import reverse
from apps.account.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'last_login', 'is_staff', 'is_active')
    list_filter = ('username', 'first_name', )

    search_fields = [
        'first_name',
        'last_name',
        'username',
        'email'
    ]

    def view_on_site(self, obj):
        return settings.SITE_URL + reverse('profile:show',
                                           args=[obj.username])

admin.site.register(User, UserAdmin)
