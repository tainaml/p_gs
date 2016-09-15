from django.contrib.auth import models


class UserManager(models.UserManager):

    def get_queryset(self):
        qs = super(UserManager, self).get_queryset()
        qs = qs.prefetch_related(
            'profile', 'profile__occupation',
            'profile__occupation__responsibility',
            #'profile__occupation__responsibility__occupation'
        )
        return qs

    def get(self, *args, **kwargs):
        user = super(UserManager, self).get(*args, **kwargs)
        return user



