from urllib import urlencode
from django.contrib.auth import get_user_model
from django.db.models import Q
from apps.custom_base.service.custom import IdeiaForm, CustomPaginator
from django import forms
from apps.gamification.models import CommunityRank


class RankingListForm(IdeiaForm):

    q = forms.CharField(required=False, max_length=255)
    community = forms.CharField(required=False, max_length=255)
    community_title = forms.CharField(required=False, max_length=255)
    page = forms.IntegerField(min_value=1, required=False)
    user = forms.IntegerField(min_value=1, required=False)


    def __init__(self, itens_per_page=10, *args, **kwargs):
        self.itens_per_page = itens_per_page
        super(RankingListForm, self).__init__(*args, **kwargs)


    @property
    def querystring(self):
        querystring_dict = {}
        for key in self.cleaned_data:
            querystring_dict[key] = unicode(self.cleaned_data[key] or '').encode('utf-8')

        return urlencode(querystring_dict)

    def clean(self):
        cleaned_data = super(RankingListForm, self).clean()
        cleaned_data['page'] = cleaned_data['page']\
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def is_valid(self):
        valid = super(RankingListForm, self).is_valid()

        return valid

    def has_key(self, key):
        return self.cleaned_data[key] if key in self.cleaned_data else None

    def __process__(self):
        queryset = CommunityRank.objects.all().order_by("rank_position")
        q = self.has_key('q')
        community = self.has_key('community')
        user = self.has_key('user')
        community_title = self.has_key('community_title')

        if q:
            queryset = queryset.filter(Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q))

        if community:
            queryset = queryset.filter(community__slug=community)

        if user:
            queryset = queryset.filter(user__id=user)

        if community_title:
            queryset = queryset.filter(community__title__icontains=community_title)

        return CustomPaginator.paginate(queryset.select_related("user", "user__profile", "community"), self.itens_per_page, self.cleaned_data['page'])

class RankingAllForm(IdeiaForm):



    page = forms.IntegerField(min_value=1, required=False)



    def __init__(self, itens_per_page=10, *args, **kwargs):
        self.itens_per_page = itens_per_page

        super(RankingAllForm, self).__init__(*args, **kwargs)


    @property
    def querystring(self):
        querystring_dict = {}
        for key in self.cleaned_data:
            querystring_dict[key] = unicode(self.cleaned_data[key] or '').encode('utf-8')

        return urlencode(querystring_dict)

    def clean(self):
        cleaned_data = super(RankingAllForm, self).clean()
        cleaned_data['page'] = cleaned_data['page']\
            if 'page' in cleaned_data and cleaned_data['page'] else 1

        return cleaned_data

    def is_valid(self):
        valid = super(RankingAllForm, self).is_valid()

        return valid

    def has_key(self, key):
        return self.cleaned_data[key] if key in self.cleaned_data else None

    def __process__(self):
        queryset = get_user_model().objects.all().order_by("-xp")


        return CustomPaginator.paginate(queryset.prefetch_related("profile"), self.itens_per_page, self.cleaned_data['page'])