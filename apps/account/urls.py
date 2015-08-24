from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^signup/', views.signup, name='signup'),
    url(r'^register/', views.register, name='register'),
    url(r'^do_login/', views.do_login, name='do_login'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^change_password/', views.change_password, name='change_password'),
    url(r'^update_password/', views.update_password, name='update_password'),
    url(r'^signup_without_captcha/', views.signup_without_captcha, name='signup_without_captcha'),
    url(r'^registered-successfully/', views.registered_successfully, name='registered_successfully')

]