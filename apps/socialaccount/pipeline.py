from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.utils.text import slugify
from requests import request, HTTPError, ConnectionError
from django.core.files.base import ContentFile
from social.pipeline.partial import partial
from apps.account.models import User

from apps.userprofile.service.business import  get_profile as GetProfile

User = get_user_model()

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
def validate_username(**kwargs):
    username = kwargs.get('username')
    if username:
        username = str(username).lower()
    users = len(User.objects.filter(username=username))
    if username and users > 0:
        kwargs['username'] = username+str(users+1)

    return kwargs

@partial
def username_slugify(**kwargs):
    if kwargs.get('username'):
        kwargs['username'] = slugify(kwargs.get('username').lower())

    return kwargs


def create_profile(strategy, user, response, details, is_new=False,*args,**kwargs):

    user.is_active = True
    user.save()
    profile = GetProfile(user)


def save_profile_picture(strategy, user, response, details, is_new=False, *args,**kwargs):
    profile = GetProfile(user)
    if not profile.profile_picture:
        if strategy.request.backend.name == 'google-oauth2':
            if response.get('image') and response['image'].get('url'):
               url = response['image'].get('url')
               url = url.split("=")[0]+"=200"
               try:
                   response = request('GET', url)
                   response.raise_for_status()
               except ConnectionError:
                   pass
               else:
                   profile.profile_picture.save('{0}_social.jpg'.format(user.username),
                                                                  ContentFile(response.content))
                   profile.save()
        if strategy.request.backend.name == 'facebook':
            url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

            try:
                response = request('GET', url, params={'type': 'large'})
                response.raise_for_status()
            except HTTPError:
                pass
            else:
                profile.profile_picture.save('{0}_social.jpg'.format(user.username),
                                                               ContentFile(response.content))
                profile.save()
