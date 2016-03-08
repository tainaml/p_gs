from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.core.views import configuration as CoreView

urlpatterns = [

    # Translators: URL de configuracao  de conta
    url(_(r'^account$'), CoreView.CoreSettingsAccountView.as_view(), name='account'),

    # Translators: URL de configuracao de notificacao
    url(_(r'^notification$'), CoreView.CoreSettingsNotificationView.as_view(), name='notification'),

    # Translators: URL de configuracao de desativar conta
    url(_(r'^deactivate-account$'), CoreView.CoreDeactivateAccountView.as_view(), name='deactivate-account'),

]