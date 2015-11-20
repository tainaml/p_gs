from django.conf.urls import url
from apps.account import views
from ..views import account as CoreViews

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^signup/$', CoreViews.CoreRegisterView.as_view(), name='signup'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^login/ajax/$', CoreViews.CoreLoginView.as_view(), name='login-ajax'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    url(r'^forgot_password/$', CoreViews.CoreForgotPassword.as_view(), name='forgot_password'),
    url(r'^registered-successfully/$', views.RegisteredSuccessView.as_view(), name='registered_successfully'),
    url(r'^mail_validation/(?P<activation_key>[0-9a-z]{40})/$', views.MailValidationView.as_view(), name='mail_validation'),
    url(r'^recovery_password/(?P<activation_key>[0-9a-z]{40})/$', views.RecoveryValidationView.as_view(), name='recovery_password'),
    url(r'^recovery_validation/(?P<activation_key>[0-9a-z]{40})/$', views.RecoveryValidationView.as_view(), name='recovery_validation'),
    url(r'^resend_account_confirmation$', views.ResendAccountConfirmationView.as_view(), name='resend_account_confirmation'),

]