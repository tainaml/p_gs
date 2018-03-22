# coding=utf-8
import json
import urllib2
from apps.account.models import User
from apps.core.business import configuration
from apps.socialactions.models import UserAction, UserActionCounter, Counter
from rede_gsti.celery import app
from apps.mailmanager.tasks import send_mail_async
from django.conf import settings
from social_django.models import UserSocialAuth


@app.task
def testing_async():
    print('Tah async mano!')


@app.task
def send_push_async(queryset, title, message, extra=None):
    if not extra:
        extra = {}
    queryset.send_message(message, title=title, extra=extra)



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
            'social_friend': social_friend.user.__dict__,
            'gender_string': gender_string,
            'user': user.__dict__
        }

        print('Pode? {}'.format(configuration.check_config_to_notify(social_friend.user, 'mail_notification', None)))

        if configuration.check_config_to_notify(social_friend.user, 'mail_notification', None):

            send_mail_async(
                to=social_friend.user.email,
                subject=subject,
                template='mailmanager/facebook-your-friend-entered.html',
                context=context
            )


@app.task
def count_user_actions(action=None):

    count = UserAction.objects.filter(object_id=action.object_id,
                                          content_type=action.content_type,
                                          action_type=action.action_type,
                                          target_user=action.target_user).count()

    #TODO REFACTOR TO A BETTER APROACH
    if action.action_type == settings.SOCIAL_LIKE:
        action.content_object.like_count = count
        action.content_object.save()
    elif action.action_type == settings.SOCIAL_UNLIKE:
        action.content_object.dislike_count = count
        action.content_object.save()
    elif action.action_type == settings.SOCIAL_COMMENT:
        action.content_object.comment_count = count
        action.content_object.save()
    else:

        count = UserAction.objects.filter(object_id=action.object_id,
                                          content_type=action.content_type,
                                          action_type=action.action_type,
                                          target_user=action.target_user).count()

        count_user = UserAction.objects.filter(action_type=action.action_type,
                                               author=action.author).count()
        try:
            counter_instance = Counter.objects.get(object_id=action.object_id,
                                                   content_type=action.content_type,
                                                   action_type=action.action_type,
                                                   target_user=action.target_user)

        except Counter.DoesNotExist:
            counter_instance = Counter(object_id=action.object_id,
                                       content_type=action.content_type,
                                       action_type=action.action_type,
                                       target_user=action.target_user)

        try:
            counter_user_instance = UserActionCounter.objects.get(action_type=action.action_type,
                                                                  author=action.author)
        except UserActionCounter.DoesNotExist:

            counter_user_instance = UserActionCounter(author=action.author, action_type=action.action_type)

        counter_instance.count=count
        counter_instance.save()
        counter_user_instance.count = count_user
        counter_user_instance.save()
