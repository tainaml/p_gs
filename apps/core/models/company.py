from apps.account.service.business import username_is_available
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

    request_user = None

    def create_user(self):

        if not self.user:

            __username = slugify(self.name)
            original_username = slugify(self.name)
            _exists = username_is_available(original_username)

            if not _exists:

                inc = 1
                while(_exists == False):
                    __username = '{}-{}'.format(original_username, inc)
                    _exists = username_is_available(__username)
                    inc = inc + 1


            company_user = User.objects.create_user(
                username=__username,
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


    def process_permissions(self):

        permissions = Membership.objects.filter(company=self)

        # If dont have admins, set current user as admin
        if permissions.filter(permission=Membership.ADMIN).count() == 0:
            try:
                current_user_in_list = permissions.get(user=self.request_user)
                current_user_in_list.permission = Membership.ADMIN
                current_user_in_list.save()
            except Exception:
                self.add_default_permission()

    def add_default_permission(self):

        member = Membership()
        member.user = self.request_user
        member.company = self
        member.permission = Membership.ADMIN
        member.save()

    def set_request_user(self, user):
        self.request_user = user

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.create_user()
        super(CompanyProxy, self).save(force_insert, force_update, using, update_fields)

        self.process_permissions()
        self.update_user()

    @classmethod
    def list_categories(cls):

        return Taxonomy.objects.filter(
            term__slug='categoria'
        )

    @classmethod
    def list_communities(cls):

        return Taxonomy.objects.filter(
            term__slug='comunidade'
        ).order_by('description')