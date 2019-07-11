from __future__ import unicode_literals

import logging


from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.shortcuts import render_to_response
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from soccer.pagingHelper import pagingHelper
from soccer.models import FreeBoard

from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.db.models import Q
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic import TemplateView

from . import models

import requests
from bs4 import BeautifulSoup


# Create your views here.
logger = logging.getLogger(__name__)

# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/


class NoJapanIdexPageView(TemplateView):
    template_name = "nojapan/index.html"
    def get_context_data(self, **kwargs):
        context = super(NoJapanIdexPageView, self).get_context_data(**kwargs)
        return context

