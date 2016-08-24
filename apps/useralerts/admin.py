from django.contrib import admin
from models import UserAlert
from admin_form import UserAlertForm


class UserAlertAdmin(admin.ModelAdmin):

    form = UserAlertForm
    filter_horizontal = ('users',)
    list_display = ['title', 'users_count', 'status']

    def users_count(self, obj):
        return obj.users.all().count()
    users_count.short_description = 'Users Count'


admin.site.register(UserAlert, UserAlertAdmin)
