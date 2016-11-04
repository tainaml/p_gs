# coding=utf-8
import json
import urllib2
from apps.account.models import User
from apps.core.business import configuration
from rede_gsti.celery import app
from social.apps.django_app.default.models import UserSocialAuth
from apps.mailmanager.tasks import send_mail_async


@app.task
def testing_async():
    print('Tah async mano!')


@app.task
def notify_by_email_user_friends(user_id):

    try:
        user = User.objects.get(id=user_id)

    except User.DoesNotExist:
        print('[ERROR] User {} does not exists'.format(user_id))
        return False

    except Exception:
        print('[ERROR] General Error on load user {} does not exists'.format(user_id))
        return False

    try:
        social_account = user.social_auth.get(provider='facebook')
    except Exception:
        print('[ERROR] User {} does not have a Facebook account linked here'.format(user.id))
        return False

    check_url = u'https://graph.facebook.com/{0}/friends?fields=id,name,email&access_token={1}'.format(
        social_account.uid,
        social_account.extra_data['access_token'],
    )

    try:
        request = urllib2.Request(check_url)
        friends = json.loads(urllib2.urlopen(request).read()).get('data')
    except Exception as e:
        print('[ERROR] General error on load friend list from Facebook: {}'.format(e))
        return False

    for friend in friends:
        try:
            social_friend = UserSocialAuth.objects.prefetch_related(
                'user'
            ).get(
                uid=friend.get('id'),
                provider='facebook'
            )
        except UserSocialAuth.DoesNotExist:
            print('[ERROR] User friend not in network')
            return False
        except Exception as e:
            print('[ERROR] General error on load user social profile: {}'.format(e))
            return False

        if not social_friend.user.email:
            print('[ERRROR] User {} does not have a email in account'.format(social_friend.user.id))
            return False

        gender_string = "Seu amigo"

        if user.user_profile.gender.lower() == 'f':
            gender_string = "Sua amiga"

        subject = '{} {} entrou no Portal GSTI'.format(
            gender_string,
            user.get_full_name()
        )

        context = {
            'social_friend': social_friend.user,
            'gender_string': gender_string,
            'user': user
        }

        print('Pode? {}'.format(configuration.check_config_to_notify(social_friend.user, 'mail_notification', None)))

        if configuration.check_config_to_notify(social_friend.user, 'mail_notification', None):

            send_mail_async(
                to=social_friend.user.email,
                subject=subject,
                template='mailmanager/facebook-your-friend-entered.html',
                context=context
            )

