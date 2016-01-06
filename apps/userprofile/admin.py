from django.contrib import admin

from apps.userprofile.models import Country, State, City, Responsibility, UserProfile

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Responsibility)
admin.site.register(UserProfile)