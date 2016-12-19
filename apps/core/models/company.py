from social.utils import slugify
from django.db.models import Q
from apps.taxonomy.models import Taxonomy
from apps.company.models import Company, CompanyContact, CompanyManager, Membership
from apps.account.models import User
from apps.userprofile.models import UserProfile


class CompanyProxyManager(CompanyManager):

    def get_queryset(self):
        qs = super(CompanyProxyManager, self).get_queryset()
        return qs.filter(
            user__usertype=User.ORGANIZATION
        )


class CompanyProxy(Company):

    class Meta:
        proxy = True

    organizations = CompanyProxyManager()

    def create_user(self):

        if not self.user:
            company_user = User.objects.create_user(
                username=slugify(self.name),
                first_name=self.name,
                last_name='',
                is_active=True,
                usertype=User.ORGANIZATION
            )

            company_user.save()

            self.user = company_user

            user_profile = self.user.user_profile
            user_profile.profile_picture = self.logo
            user_profile.description = self.description
            user_profile.save()

        return self.user

    def update_user(self):

        if not self.user:
            return None

        self.user.first_name = self.name
        self.user.save()

        try:

            user_profile = UserProfile.objects.get(user=self.user)
            user_profile.profile_picture = self.logo
            user_profile.description = self.description
            user_profile.save()

        except Exception as e:
            print(e)

    def add_default_permission(self):

        member = Membership()
        member.user = self.user
        member.company = self
        member.permission = Membership.ADMIN
        member.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.create_user()
        super(CompanyProxy, self).save(force_insert, force_update, using, update_fields)

        if self.members.count() == 0:
            self.add_default_permission()

        self.update_user()

    @classmethod
    def list_categories(cls):

        return Taxonomy.objects.filter(
            term__slug='categoria'
        )

    @classmethod
    def list_communities(cls):

        return Taxonomy.objects.filter(
            term__slug='comunidade',
            parent__term__slug='comunidade'
        ).order_by('description')