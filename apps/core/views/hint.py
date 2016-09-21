from apps.account.models import User
from apps.socialactions.service import business as SocialActionsBusiness
from django.conf import settings
from django.db.models import Q
from django.db.models.query import Prefetch
from django.http.response import JsonResponse, Http404, HttpResponseBadRequest
from django.views.generic import View
from apps.comment.service import business as CommentBusiness
from apps.core.business import user as UserBusiness


class HintAjaxView(View):

    request = None
    instance_type = None
    instance_id = None
    content_object = None

    def get_object_author(self, content_object=None):

        content_object = content_object if content_object else self.content_object

        try:
            return content_object.author_id
        except Exception as e:
            return None

    def get_comments_authors(self, content_object):

        all_comments = CommentBusiness.get_all_comments_by_content_object(content_object)
        all_comments = all_comments.only('author_id').distinct()

        __authors = []
        for comment in all_comments:
            __authors.append(
                comment.author_id
            )

        return __authors

    def get_current_user(self):
        try:
            return self.request.user
        except Exception:
            return None

    def get_following(self):

        try:
            actions = SocialActionsBusiness.get_users_acted_by_author(
                author=self.get_current_user(),
                action=settings.SOCIAL_FOLLOW,
                content_type='user',
            )

            following = []
            for item in actions:
                following.append(item.object_id)

            return following

        except Exception as e:
            print('Error on get_author_following: {}'.format(e.message))
            return False

    def get_answer_related_users(self):

        users = []

        try:
            question = self.content_object.question
            users.append(question.author_id)

            answers = question.question_owner.all().exclude(id=self.content_object.id)

            for answer in answers:
                comment_users = self.get_comments_authors(answer)
                if comment_users:
                    users += comment_users

                # Answer author
                answer_author = self.get_object_author(answer)
                if answer_author:
                    users.append(answer_author)

        except Exception as e:
            print('{}'.format(e.message))

        return users

    def get(self, request, instance_type, instance_id):

        self.request = request
        self.instance_type = instance_type
        self.instance_id = instance_id


        term_filter = request.GET.get('term', None)

        if not term_filter:
            return HttpResponseBadRequest()

        content_object = CommentBusiness.get_content_object_by_content_type_and_id(
            self.instance_type,
            self.instance_id
        )

        self.content_object = content_object

        all_users = []

        author = self.get_object_author()
        if author:
            all_users.append(author)

        # All users has commented
        all_users += self.get_comments_authors(self.content_object)

        # Current logged user
        current_user = self.get_current_user()
        if current_user:
            all_users.append(current_user.id)

        # User is following
        following = self.get_following()
        if following:
            all_users += following

        if instance_type == 'answer':
            all_users += self.get_answer_related_users()


        # Clean and remove duplicates
        all_users = list(set(all_users))

        users = User.objects.only('first_name', 'last_name', 'username').filter(
            Q(
                Q(id__in=all_users) &
                (Q(first_name__unaccent__icontains=term_filter) | Q(last_name__unaccent__icontains=term_filter))
            )
        ).distinct()

        users_to_return = []
        for user in users:

            avatar_url = user.user_profile.avatar_url
            thumbor_media_url = getattr(settings, 'THUMBOR_MEDIA_URL', None)
            thumbor_url = getattr(settings, 'THUMBOR_URL', None)

            if thumbor_url:
                #avatar_url = user.user_profile.profile_picture.name
                avatar_url = '{}/{}'.format(
                    thumbor_url,
                    avatar_url
                )

            users_to_return.append({
                'full_name': user.get_full_name(),
                'username': user.username,
                'thumb_url': avatar_url
            })

        context = {
            'users': users_to_return
        }

        return JsonResponse(context)
