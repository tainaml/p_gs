from django.db import transaction
from apps.userprofile.service import business as BusinessUserProfile

@transaction.atomic
def save_profile(user):
    profile = BusinessUserProfile.check_profile_exists(user)
    user.username = str(user.username.lower())
    user.save()
    return profile
