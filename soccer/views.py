from __future__ import unicode_literals

import logging


from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic import TemplateView

from . import models
from . import serializers
from .forms import ContactForm, FilesForm, ContactFormSet

# Create your views here.
logger = logging.getLogger(__name__)

# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/



class IndexPageView(TemplateView):
    template_name = "soccer/index.html"

    def get_match_datas(self):
        matchs = []
        objs = models.Matchs.objects.all()
        for obj in objs:
            logger.debug("match : %s (%s)" % (obj, obj.date))
        return matchs

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        self.get_match_datas()
        context['matchs'] = models.Matchs.objects.order_by('-date')
        return context

#-----------------------------------------------------------------------------------------------------------------------
class FakeField(object):
    storage = default_storage
fieldfile = FieldFile(None, FakeField, "dummy.txt")

class HomePageView(TemplateView):
    template_name = "soccer/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, "hello http://example.com")
        return context


class DefaultFormsetView(FormView):
    template_name = "soccer/formset.html"
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = "soccer/form.html"
    form_class = ContactForm


class DefaultFormByFieldView(FormView):
    template_name = "soccer/form_by_field.html"
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = "soccer/form_horizontal.html"
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = "soccer/form_inline.html"
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = "soccer/form_with_files.html"
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context["layout"] = self.request.GET.get("layout", "vertical")
        return context

    def get_initial(self):
        return {"file4": fieldfile}


class PaginationView(TemplateView):
    template_name = "soccer/pagination.html"

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(200):
            lines.soccerend("Line %s" % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get("page")
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context["lines"] = show_lines
        return context


class MiscView(TemplateView):
    template_name = "soccer/misc.html"
