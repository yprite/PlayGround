# Create your views here.
# goaccess /var/log/apache2/playfun.log --log-format=COMBINED -a -o report.html

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from django.http import Http404, HttpResponse

from . import utils


logger = logging.getLogger(__name__)

def index(request):
    html = utils.get_goaccess_html()
    if not html:
        raise Http404('GoAccess report page not found.')
    return HttpResponse(html)

