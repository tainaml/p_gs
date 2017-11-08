from apps.api.custom_permissions import IsSelf
from apps.api.serializers.user import UserProfileSerializer, UserSerializer, UserWithoutEmailSerializer
from django.contrib.auth import get_user_model
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from ..pagination import StandardResultsSetPagination
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated, IsSelf)
    authentication_classes = (OAuth2Authentication, SessionAuthentication)

    parser_classes = (FormParser, MultiPartParser)



    @method_decorator(cache_page(30))
    def dispatch(self, request, *args, **kwargs):
        return super(UserViewSet, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            user = self.request.user

            self.serializer_class = UserProfileSerializer if not user.email else UserWithoutEmailSerializer
            return self.request.user

        return super(UserViewSet, self).get_object()


    def partial_update(self, request, pk=None, *args, **kwargs):
        return super(UserViewSet, self).partial_update(request, pk, *args, **kwargs)

    def perform_update(self, serializer):
        instance = self.get_object()
        instance.wizard_step = 1

        serializer.save()
        instance.save()

    def update(self, request, pk=None, *args, **kwargs):
        return super(UserViewSet, self).update(request, pk, *args, **kwargs)



