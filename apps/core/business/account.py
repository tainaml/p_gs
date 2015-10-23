from apps.userprofile.service import business as BusinessUserProfile


def save_profile(user):
    profile = BusinessUserProfile.check_profile_exists(user)
    return profile