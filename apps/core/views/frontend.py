from django.shortcuts import render
from django.views.generic import View

class FrontEndBase(View):

    def get(self, request, template):

        template_name = "front_end/%s" % template
        context = {}
        return render(request, template_name, context)
