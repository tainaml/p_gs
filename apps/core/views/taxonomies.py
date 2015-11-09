import json
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.views.generic import View
from apps.taxonomy.models import Taxonomy, Term
from apps.community.models import Community
from django.db.models import Q

class CoreUserCategoriesView(View):

    def get(self, request):



        return HttpResponse(json.dumps({}), content_type='application/json')