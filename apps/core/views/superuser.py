#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import render
from django.views import View
from apps.core.forms.superuser import SearchNotificationSubscribe, NotificationSend

__author__ = 'phillip'

#TODO put it into a decorator
def is_admin(user):
    return user.is_authenticated() and user.is_superuser


class AdminPush(View):

    template_name = 'superuser/push.html'
    context = {}
    form = SearchNotificationSubscribe
    form_send = NotificationSend

    def get(self, request):

        if not is_admin(request.user):
            raise Http404()

        self.form =  self.form(request.GET)
        items = self.form.process()

        self.form_send = self.form_send(initial=self.form.cleaned_data)

        self.context.update({
            'form': self.form,
            'items': items,
            'form_send': self.form_send
        })
        return render(request, self.template_name, self.context)

    def post(self, request):

        if not is_admin(request.user):
            raise Http404()

        self.form =  self.form(request.POST)
        items = self.form.process()

        self.form_send = self.form_send(request.POST)

        try:
            if self.form_send.process():
                self.context.update({'success_message': "Enviado para %s inscritos" % str(items)})
            else:
                self.context.update({'error_message': "Certifique-se de que todos os campos estão preenchidos e que a url informada é uma url válida"})
        except Exception as e:
            self.context.update({'error_message': "Um erro ocorreu ao tentar enviar as mensagens: %s" % str(e)})

        self.context.update({
            'form': self.form,
            'items': items,
            'form_send': self.form_send
        })
        return render(request, self.template_name, self.context)