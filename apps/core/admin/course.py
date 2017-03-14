from bs4 import BeautifulSoup
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.utils import unquote
from django.utils.translation import ugettext as _
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.text import slugify
from apps.core.models.rating import Rating
from django import forms
from django.contrib import admin
from django.contrib.admin import StackedInline
from ideia_summernote.widget import SummernoteWidget
from apps.core.models.course import Course, Curriculum
from apps.core.models.plataform import Plataform
from django.contrib.contenttypes.admin import GenericStackedInline
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin import helpers
from django.forms.formsets import all_valid

csrf_protect_m = method_decorator(csrf_protect)

IS_POPUP_VAR = '_popup'
TO_FIELD_VAR = '_to_field'

class CurruculumAdminInlineForm(forms.ModelForm):


    class Meta:
        model = Curriculum
        exclude = ()
        widgets = {
            'description': SummernoteWidget(editor_conf='article_admin')
        }


class CurriculumInline(StackedInline):

    form = CurruculumAdminInlineForm

    model = Curriculum
    # extra = 0
    # min_num = 1




class RatingsInline(GenericStackedInline):

    model = Rating
    extra = 1
    raw_id_fields = ['author']

class ModelFormAdminCourse(forms.ModelForm):


    class Meta:
        model = Course
        exclude = ('rating',)
        widgets = {
            'observation': SummernoteWidget(editor_conf='article_admin')
        }





class CoreCourseAdmin(admin.ModelAdmin):

    list_display = ('title', 'rating', 'internal_author', 'updatein')
    list_display_links = list_display

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(CoreCourseAdmin, self).get_formset(request, obj, **kwargs)
        # formset.request = request
        return formset

    def make_request(self, url):
        content = None
        import requests
        response = requests.get(url=url)
        if response.status_code in [200, 304]:
            content = response.content

        return content

    def get_udemy_curriculum(self, content):
        initial = []
        soup = BeautifulSoup(content, "html.parser")
        curriculums = soup.select(".content-container")

        for curriculm in curriculums:

            title = curriculm.select(".lecture-title-text")[0].get_text().strip()
            curriculm_dict = {'title': title}
            description = '<ul>'
            for title in curriculm.select(".left-content"):
                description+= '<li>%s</li>' % title.get_text().strip()
            description+='</ul>'
            curriculm_dict['description'] = description

            initial.append(curriculm_dict)


        return initial


    def get_udemy_course(self, content):
        initial_data = {}

        soup = BeautifulSoup(content, "html.parser")
        initial_data['title'] =  soup.h1.get_text().strip()
        initial_data['slug'] =  slugify(soup.h1.get_text().strip())

        #DEscription
        initial_data['description'] = ''
        for description in soup.select(".js-simple-collapse--description"):
            initial_data['description']+= description.get_text().strip()[:400]

        #Author
        initial_data['external_author'] = ''
        for external_author in soup.select(".instructor__title"):
            initial_data['external_author']+= external_author.get_text().strip()


        #Author
        initial_data['external_author_description'] = ''
        for external_author_description in soup.select(".instructor__expand-description"):
            initial_data['external_author_description']+= external_author_description.get_text().strip()[:255]

        #Platform
        try:
            initial_data['plataform'] = Plataform.objects.get(slug='udemy')
        except Plataform.DoesNotExist:
            pass


        return initial_data





    inlines = [CurriculumInline]
    form = ModelFormAdminCourse

    class Meta:
        widgets = {
            'observation': SummernoteWidget(editor_conf='article_admin')
        }


    @csrf_protect_m
    @transaction.atomic
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):

        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        model = self.model
        opts = model._meta

        if request.method == 'POST' and '_saveasnew' in request.POST:
            object_id = None

        add = object_id is None

        if add:
            if not self.has_add_permission(request):
                raise PermissionDenied
            obj = None

        else:
            obj = self.get_object(request, unquote(object_id), to_field)

            if not self.has_change_permission(request, obj):
                raise PermissionDenied

            if obj is None:
                raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                    'name': force_text(opts.verbose_name), 'key': escape(object_id)})

        ModelForm = self.get_form(request, obj)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=not add)
            else:
                form_validated = False
                new_object = form.instance
            formsets, inline_instances = self._create_formsets(request, new_object, change=not add)
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, not add)
                self.save_related(request, form, formsets, not add)
                change_message = self.construct_change_message(request, form, formsets, add)
                if add:
                    self.log_addition(request, new_object, change_message)
                    return self.response_add(request, new_object)
                else:
                    self.log_change(request, new_object, change_message)
                    return self.response_change(request, new_object)
            else:
                form_validated = False
        else:
            if add:
                initial = self.get_changeform_initial_data(request)
                form = ModelForm(initial=initial)
                formsets, inline_instances = self._create_formsets(request, form.instance, change=False)
            else:
                form = ModelForm(instance=obj)
                formsets, inline_instances = self._create_formsets(request, obj, change=True)

        adminForm = helpers.AdminForm(
            form,
            list(self.get_fieldsets(request, obj)),
            self.get_prepopulated_fields(request, obj),
            self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        if 'udemy_url' in request.GET:
            content = self.make_request(request.GET['udemy_url'])
            initial_data = self.get_udemy_course(content)

            adminForm.form.initial = initial_data

            for f in formsets:
                initial_curriculums = self.get_udemy_curriculum(content)
                f.extra = len(initial_curriculums)
                f.initial_extra = initial_curriculums



        inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
        for inline_formset in inline_formsets:
            media = media + inline_formset.media



        context = dict(
            self.admin_site.each_context(request),
            title=(_('Add %s') if add else _('Change %s')) % force_text(opts.verbose_name),
            adminform=adminForm,
            object_id=object_id,
            original=obj,
            is_popup=(IS_POPUP_VAR in request.POST or
                      IS_POPUP_VAR in request.GET),
            to_field=to_field,
            media=media,
            inline_admin_formsets=inline_formsets,
            errors=helpers.AdminErrorList(form, formsets),
            preserved_filters=self.get_preserved_filters(request),
        )

        # Hide the "Save" and "Save and continue" buttons if "Save as New" was
        # previously chosen to prevent the interface from getting confusing.
        if request.method == 'POST' and not form_validated and "_saveasnew" in request.POST:
            context['show_save'] = False
            context['show_save_and_continue'] = False
            # Use the change template instead of the add template.
            add = False

        context.update(extra_context or {})

        return self.render_change_form(request, context, add=add, change=not add, obj=obj, form_url=form_url)

admin.site.register(Course, CoreCourseAdmin)
admin.site.register(Plataform)