from django.shortcuts import redirect
from django.utils.text import slugify

from social.pipeline.partial import partial


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            return redirect('require_email')


@partial
def username_slugify(**kwargs):
    print kwargs
    if kwargs.get('username'):
        kwargs['username'] = slugify(kwargs.get('username').lower())

    return kwargs