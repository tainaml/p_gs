from apps.account.models import User, UserManager


class CompanyUserManager(UserManager):

    def get_queryset(self):
        qs = super(CompanyUserManager, self).get_queryset()
        return qs.filter(
            usertype=User.ORGANIZATION
        )


class CompanyUser(User):

    objects = CompanyUserManager()

    def save(self, *args, **kwargs):
        self.usertype = User.ORGANIZATION
        return super(CompanyUser, self).save(*args, **kwargs)

    class Meta:
        proxy = True
