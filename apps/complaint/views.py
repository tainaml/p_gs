from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.utils.translation import ugettext as _

from apps.feed.models import FeedObject
from apps.complaint.service.form import ComplaintForm
from apps.complaint.service import business as Business
from rede_gsti import settings


class ComplaintView(View):
    template_path = "complaint/report.html"
    form_complaint = ComplaintForm

    def response(self, request, status, context=None):
        if not context:
            context = {}

        if request.is_ajax():
            _context = {
                'message': context.get('message'),
                'template': render(request, self.template_path, context).content
            }
            return JsonResponse(_context, status=status)

        return render(request, self.template_path, context)

    @method_decorator(login_required)
    def get(self, request, object_type, object_id):

        status = 200
        context = {
            'community_complaint': settings.COMPLAINT_COMMUNITY,
            'type_complaint': Business.get_type_complaint(),
            'communities': None
        }

        try:
            content_type = ContentType.objects.get(model=object_type)
            content_object = content_type.get_object_for_this_type(id=object_id)

            context.update({
                'content_object': content_object,
                'content_type': content_type
            })

            try:
                feed = FeedObject.objects.get(
                    object_id=content_object.id,
                    content_type=content_type
                )

                communities = feed.communities.all()
                context.update({'communities': communities})

            except Exception, e:
                context.update({'message': e.message})


        except Exception, e:
            context.update({'message': e.message})
            status = 400

        return self.response(request, status, context)

    @method_decorator(login_required)
    def post(self, request, object_type, object_id):

        form = self.form_complaint(request.user, request.POST)

        if not form.process():
            message = _("Complaint not created!")
            context = {
                'message': message,
                'errors': form.errors
            }
            return JsonResponse(context, status=400)

        message = _("Complaint created successfully!")
        context = {'message': message}
        return JsonResponse(context, status=200)