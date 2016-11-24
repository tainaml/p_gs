from abc import ABCMeta, abstractmethod
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django import forms
from apps.account.models import User


class SelectizeRegistrator(object):

    __mapper = {}

    def add_item(self, key, queryset, value_field='id', label_field='id', search_fields=None):

        if not self.__mapper.has_key(key):
            self.__mapper.update({
                key: {
                    'queryset': queryset,
                    'value_field': value_field,
                    'label_field': label_field,
                    'search_fields': search_fields
                }
            })

    def get_item(self, key):
        return self.__mapper.get(key, None)


register = SelectizeRegistrator()


class SelectizeValidationForm(forms.Form):

    q = forms.CharField(max_length=100, min_length=3)


class SelectizeAutomatic(View):

    def get(self, request, unique_name):

        form = SelectizeValidationForm(data=request.GET)

        context = {
            'unique_name': unique_name,
        }

        if not form.is_valid():
            return JsonResponse(context, status=400)

        term = form.cleaned_data.get('q')

        field_obj =  register.get_item(unique_name)

        search_keys = field_obj.get('search_fields')

        value_field = field_obj.get('value_field')
        label_field = field_obj.get('label_field')

        search_criteria = Q()
        for key in search_keys:
            qriteria = {
                '{}'.format(key): term
            }
            search_criteria = search_criteria | Q(**qriteria)

        items = []
        qs = field_obj.get('queryset')

        try:
            if qs:
                items_qs = qs.filter(search_criteria)[:10]
                items = [{'value': getattr(it, value_field), 'label': getattr(it, label_field)} for it in items_qs if hasattr(it, value_field) and hasattr(it, label_field)]
        except Exception as e:
            print('Error in selectize: {}'.format(e))

        context.update({
            'items': items
        })

        return JsonResponse(context, status=200)


class SelectizeBaseView(View):

    __metaclass__ = ABCMeta

    value_field = 'id'
    label_field = 'id'
    search_field = 'name'

    limit = 10
    model = None
    form_class = SelectizeValidationForm
    _form = None

    def get_queryset(self, form):
        if not self.model:
            return None

        query = {
            '{}__unaccent__icontains'.format(self.search_field): form
        }

        return self.model.objects.all().filter(
            **query
        )[:self.limit]

    def get(self, request):

        form = self.form_class(request.GET)

        if not form.is_valid():
            return JsonResponse({}, status=400)

        qs = self.get_queryset(form)

        _data = []

        for item in qs:
            _data.append({
                'value': item[self.value_field],
                'label': item[self.label_field],
            })

        return JsonResponse(_data, status=200)


class AuthorSelectize(SelectizeBaseView):

    model = User
    search_field = None

