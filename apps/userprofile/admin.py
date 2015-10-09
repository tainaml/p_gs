from django.contrib import admin

from apps.userprofile.models import Country, State, City, Responsibility

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Responsibility)