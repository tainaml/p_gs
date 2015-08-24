from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^signup/', views.signup, name='signup'),
    url(r'^register/', views.register, name='register'),
    url(r'^registered-successfully/', views.registered_successfully, name='registered_successfully')

]