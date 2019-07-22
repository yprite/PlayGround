from __future__ import unicode_literals

import logging


from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.shortcuts import render_to_response
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import JsonResponse

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
        context['categories'] = models.category.objects.all()
        context['companies'] = models.company.objects.all()
        categories = []
        for company in models.company.objects.all():
            category_string = ""
            for category in company.category.all():
                category_string = category_string + "#" + str(category.name) + " "
            categories.append(category_string)

        context['company_categories'] = categories

        context['company_ids'] = []
        for i in models.company.objects.values_list('id'):
            context['company_ids'].append(i[0])

        return context

def description(request, id):
    def clean_html_tag(raw_html):
        import re
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    company = get_object_or_404(models.company, id=id)
    session = requests.Session()
    content = BeautifulSoup(session.get(company.wiki).text, 'html.parser')
    desc = clean_html_tag(content.find('div', id='mw-content-text').find('div', class_="mw-parser-output").find('p').text) if company.wiki else ""
    
    data = {
            'id'    : company.id,
            'desc'  : desc[:200] + "..." if len(desc) > 200 else desc
    }
    return JsonResponse(data)
    '''
        descriptions = []
        for company in models.company.objects.all():
            if company.wiki:
                session = requests.Session()
                content = BeautifulSoup(session.get(company.wiki).text, 'html.parser')
                descriptions.append (clean_html_tag(content.find('div', id='mw-content-text').find('div',
                    class_="mw-parser-output").find('p').text))
            else:
                descriptions.append("")
        print (len(context['companies']))
        print (len(descriptions))
        content['descriptions'] = descriptionsA
    '''
