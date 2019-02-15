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


# Create your views here.
logger = logging.getLogger(__name__)

class IndexPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        return context

# Create your views here.
