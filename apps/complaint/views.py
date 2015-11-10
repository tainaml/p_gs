from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib import messages
from django.core.urlresolvers import reverse
from apps.article.service import business as business_article
from apps.complaint.service.form import ComplaintForm
from django.utils.translation import ugettext as _
from apps.feed.models import FeedObject
from rede_gsti import settings


class ComplaintView(View):

    form_complaint = ComplaintForm

    @method_decorator(login_required)
    def get(self, request, complaint):
        article = business_article.get_article(complaint)
        content_type = ContentType.objects.filter(model="article")
        feed_object = FeedObject.objects.filter(
            article=article,
            content_type=content_type
        ).first()
        communities = feed_object.communities.all()
        context = {'article': article, 'communities': communities}

        return render(request, 'complaint/test_complaint.html', context)

    @method_decorator(login_required)
    def post(self, request, complaint):

        article = business_article.get_article(complaint)
        context = {'article': article}
        form = self.form_complaint(request.user, request.POST)
        if not form.process():
            messages.add_message(request, messages.WARNING, _("Complaint not created!"))
        else:
            messages.add_message(request, messages.SUCCESS, _("Complaint created successfully!"))
            return redirect(reverse('question:show', args=(form.instance.id,)))

        return render(request, 'complaint/test_complaint.html', context)