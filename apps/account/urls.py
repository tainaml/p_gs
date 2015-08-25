from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^register/$', views.register, name='register'),
    url(r'^do_login/', views.do_login, name='do_login'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^change_password/', views.change_password, name='change_password'),
    url(r'^update_password/', views.update_password, name='update_password'),
    url(r'^forgot_password/$', views.forgot_password, name='forgot_password'),
    url(r'^do_forgot_password/$', views.do_forgot_password, name='do_forgot_password'),
    url(r'^signup_without_captcha/$', views.signup_without_captcha, name='signup_without_captcha'),
    url(r'^registered-successfully/$', views.registered_successfully, name='registered_successfully'),
    url(r'^mail_validation/(?P<activation_key>[0-9a-z]{40})/$', views.mail_validation, name='mail_validation'),
    url(r'^recovery_password/(?P<activation_key>[0-9a-z]{40})/$', views.recovery_validation, name='recovery_validation'),
    url(r'^do_recovery_validation/$', views.do_recovery_validation, name='do_recovery_validation'),

]