from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.account import views
from ..views import account as CoreViews

urlpatterns = [


    # Translators: URL de pagina de inscricao
    url(_(r'^inscricao/$'), CoreViews.CoreRegisterView.as_view(), name='signup'),

    # Translators: URL de pagina de login
    url(_(r'^login/$'), views.LoginView.as_view(), name='login'),

    # Translators: URL de pagina de login ajax
    url(_(r'^login/ajax/$'), CoreViews.CoreLoginView.as_view(), name='login-ajax'),

    # Translators: URL de pagina de logout
    url(_(r'^logout/'), views.LogoutView.as_view(), name='logout'),

    # Translators: URL de pagina de servico que verifica se usuario esta logado
    url(_(r'^is-logged/'), views.IsLogged.as_view(), name='is_logged'),

    # Translators: URL de pagina de mudanca de senha
    url(_(r'^change_password$'), CoreViews.CoreChangePassword.as_view(), name='change_password'),

    # Translators: URL de pagina de esquecimento de senha
    url(_(r'^forgot_password$'), CoreViews.CoreForgotPassword.as_view(), name='forgot_password'),

    # Translators: URL de pagina de registro com sucesso
    url(_(r'^registered-successfully/$'), views.RegisteredSuccessView.as_view(), name='registered_successfully'),

    # Translators: URL de pagina de validacao de email
    url(_(r'^mail_validation/(?P<activation_key>[0-9a-z]{40})/$'), views.MailValidationView.as_view(), name='mail_validation'),

    # Translators: URL de pagina de recuperacao de senha com sucesso
    url(_(r'^recovery-password/successfully/$'), views.RecoveryPasswordSuccessView.as_view(), name='recovery_successfully'),

    # Translators: URL de pagina de recuperacao de senha
    url(_(r'^recovery_password/(?P<activation_key>[0-9a-z]{40})/$'), views.RecoveryValidationView.as_view(), name='recovery_password'),

    # Translators: URL de pagina de validacao de recuperacao
    url(_(r'^recovery_validation/(?P<activation_key>[0-9a-z]{40})/$'), views.RecoveryValidationView.as_view(), name='recovery_validation'),

    # Translators: URL de pagina de reenvio de confirmacao de conta
    url(_(r'^resend_account_confirmation$'), CoreViews.CoreResendAccountConfirmationView.as_view(), name='resend_account_confirmation'),

    # Translators: URL de pagina de check de username
    url(_(r'^check-username$'), views.CheckUsernameView.as_view(), name='check-username')

]