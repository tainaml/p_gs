from django.shortcuts import render

from ..forms.account import CoreSignUpForm
from apps.account import views

class CoreArticleEditView(views.RegisterView):

    form = CoreSignUpForm