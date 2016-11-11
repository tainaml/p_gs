from apps.article.models import Article
from apps.community.models import Community
from django import forms
from apps.custom_base.service.custom import IdeiaForm
from apps.taxonomy.service import business as TaxonomyBusiness
from django.core import paginator
from django.db.models.query_utils import Q
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


class VideosFiltersForm(IdeiaForm):

    ORDER_BY_NEW_FIRST = 1
    ORDER_BY_OLD_FIRST = 2
    ORDER_BY_LIKES_ASC = 3
    ORDER_BY_LIKES_DESC = 4

    CHOICES_ORDER_BY = (
        (0, _('Default')),
        (ORDER_BY_NEW_FIRST, _('Recent')),
        (ORDER_BY_OLD_FIRST, _('Oldest')),
        (ORDER_BY_LIKES_ASC, _('Likes Asc')),
        (ORDER_BY_LIKES_DESC, _('Likes Desc'))
    )

    page = forms.IntegerField(required=False)
    criteria = forms.CharField(required=False)
    category = forms.IntegerField(required=False)
    community = forms.IntegerField(required=False)
    order = forms.ChoiceField(choices=CHOICES_ORDER_BY, required=False)

    items_per_page = 12

    def clean_criteria(self):
        criteria = self.cleaned_data.get('criteria', '')
        criteria = slugify(criteria)
        return criteria

    def clean_page(self):
        page = self.cleaned_data.get('page', 1)
        if not page:
            page = 1
        return page

    def clean_order(self):
        order = self.cleaned_data.get('order')
        try:
            return int(order)
        except Exception:
            return 0

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category and TaxonomyBusiness.get_categories(list_ids=[category]).count() > 0:
            return category
        else:
            self.cleaned_data.pop('category')
            return ''

    def clean_community(self):
        community = self.cleaned_data.get('community')
        category = self.cleaned_data.get('category')

        try:

            qs = Community.objects.all()

            if category:
                qs = self.get_communities(category)

            community_obj = qs.get(id=community)
            return community
        except Community.DoesNotExist:
            self.cleaned_data.pop('community')
        except Exception:
            pass

        return ''

    def get_categories(self):
        return TaxonomyBusiness.get_categories().order_by('description')

    def get_communities(self, category=None):

        communities = Community.objects.all()

        if category:
            communities = communities.filter(
                Q(taxonomy__in=[category]) | Q(taxonomy__parent__in=[category])

            )
        else:
            communities = Community.objects.none()

        return communities.order_by('title')

    def __process__(self):

        page = self.cleaned_data.get('page')
        order = self.cleaned_data.get('order')

        qs = Article.objects.filter(
            status=Article.STATUS_PUBLISH,
            feed__tags__tag_slug='video'
        ).prefetch_related(
            'feed', 'author'
        ).order_by('-publishin')

        category = self.cleaned_data.get('category')
        criteria = self.cleaned_data.get('criteria')
        community = self.cleaned_data.get('community')

        if category:
            qs = qs.filter(feed__taxonomies__in=[category])

        if community and category:
            qs = qs.filter(feed__communities__in=[community])

        if criteria:
            qs = qs.filter(title__unaccent__icontains=criteria)

        if order and order == self.ORDER_BY_NEW_FIRST:
            qs = qs.order_by('-publishin')

        if order and order == self.ORDER_BY_OLD_FIRST:
            qs = qs.order_by('publishin')

        if order and order == self.ORDER_BY_LIKES_ASC:
            qs = qs.order_by('like_count')

        if order and order == self.ORDER_BY_LIKES_DESC:
            qs = qs.order_by('-like_count')

        paginated = paginator.Paginator(qs, self.items_per_page)

        try:
            items = paginated.page(page)
        except Exception:
            items = paginated.page(1)

        return items
