import json

from django.http import HttpResponse
from django.views.generic import View


class CoreUserCategoriesView(View):

    def get(self, request):



        return HttpResponse(json.dumps({}), content_type='application/json')