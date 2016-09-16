from django.contrib.auth import models


class UserManager(models.UserManager):

    prefetch_fields = [
        'profile', 'profile__occupation',
        'profile__occupation__responsibility',
    ]

    def get_queryset(self):
        qs = super(UserManager, self).get_queryset()
        qs = qs.prefetch_related(*self.prefetch_fields).select_related('profile')
        return qs
