from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^register/$', views.register, name='register'),
    url(r'^signup_without_captcha/$', views.signup_without_captcha, name='signup_without_captcha'),
    url(r'^registered-successfully/$', views.registered_successfully, name='registered_successfully'),
    url(r'^mail_validation/(?P<activation_key>[0-9a-z]{40})/$', views.mail_validation, name='mail_validation'),
    url(r'^recovery_validation/(?P<activation_key>[0-9a-z]{40})/$', views.recovery_validation, name='recovery_validation'),

]