# coding=utf-8
import urllib
from django.http import QueryDict
from django.shortcuts import render
from django.views import View
from apps.core.forms.videos import VideosFiltersForm


class VideoView(View):

    template_path = 'videos/page.html'
    template_items = 'videos/items.html'
    form = VideosFiltersForm

    def get_context(self, request):

        form = self.form(
            data=request.GET
        )

        videos = form.process()

        if videos == False:
            videos = form.empty_querystring()

        form_data = form.cleaned_data
        if videos.has_next():
            form_data.update({
                'page': videos.next_page_number()
            })

        next_querystring = urllib.urlencode(form_data)

        return {
            'form': form,
            'videos': videos,
            'order_choices': form.CHOICES_ORDER_BY,
            'categories': form.get_categories(),
            'communities': form.get_communities(form_data.get('category', 0)),
            'next_querystring': next_querystring
        }

    def get(self, request):

        context = self.get_context(request)

        template = self.template_path

        if request.is_ajax():
            template = self.template_items

        return render(
            request,
            template_name=template,
            context=context
        )
