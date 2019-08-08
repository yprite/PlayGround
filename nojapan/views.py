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

from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView

from .forms import AddReplaceForm

import sys

class AddReplaceView(BSModalUpdateView):
    model = models.company
    template_name = 'nojapan/update.html'
    form_class = AddReplaceForm
    success_message = 'Success: update'
    success_url = reverse_lazy('nojapan_index')

    '''
    def get_success_message(self, cleaned_data):
        try:
            product = models.product.objects.get(name=cleaned_data['name'])
            if product:
                company_id = self.kwargs.get('id')
                company = models.company.objects.get(id=company_id)
                replace, is_created = models.product.objects.get_or_create(name=cleaned_data['name'])
                company.replace.add(replace)
                company.save()
        except Exception as E:
            print ("%s : %s" % (sys._getframe().f_code, E))
        instance = super(AddReplaceView, self).get_success_message(cleaned_data)
        return instance
    def dispatch(self, request, *args, **kwargs):
        print ("A:",sys._getframe().f_code)
        response = super(AddReplaceView, self).dispatch(request, *args, **kwargs)
        print ("B:",sys._getframe().f_code)
        return response
    def get_success_url(self):
        print ("A:",sys._getframe().f_code)
        print ("B:",sys._getframe().f_code)
        return self.success_url

    def form_valid(self, form):
        print ("A:",sys._getframe().f_code)
        response = super(AddReplaceView, self).form_valid(form)
        print ("B:",sys._getframe().f_code)
        return response

    def get_success_message(self, cleaned_data):
        print ("A:",sys._getframe().f_code)
        print (self._allowed_methods)
        print (cleaned_data)
        instance = super(AddReplaceView, self).get_success_message(cleaned_data)
        print ("B:",sys._getframe().f_code)
        return instance

    def options(self, request, *args, **kwargs):
        print ("A:",sys._getframe().f_code)
        options = super(AddReplaceView, self).options(request, *args, **kwargs)
        print ("B:",sys._getframe().f_code)
        return options
    
    def get(self, request, *args, **kwargs):
        print ("A:",sys._getframe().f_code)
        instance = super(AddReplaceView, self).get(request, *args, **kwargs)
        print ("B:",sys._getframe().f_code)
        return instance
    
    def post(self, request, *args, **kwargs):
        print ("A:",sys._getframe().f_code)
        instance = super(AddReplaceView, self).post(request, *args, **kwargs)
        print ("B:",sys._getframe().f_code)
        return instance

    def render_to_response(self, context, **response_kwargs): 
        print ("A:",sys._getframe().f_code)
        instance = super(AddReplaceView, self).render_to_response(context, **response_kwargs)
        print ("B:",sys._getframe().f_code)
        return instance
    '''

class NoJapanIdexPageView(TemplateView):
    template_name = "nojapan/index.html"
    def get_context_data(self, **kwargs):
        context = super(NoJapanIdexPageView, self).get_context_data(**kwargs)
        context['categories'] = models.category.objects.all()
        context['companies'] = models.company.objects.all()
        company_categories = []
        company_replaces = []
        for company in models.company.objects.all():
            categories = ""
            replaces = []
            for category in company.category.all():
                categories = categories + "#" + str(category.name) + " "
            company_categories.append(categories)

            if company.replace is None:
                company_replaces.append([])
            else:
                for replace in str(company.replace).split(','):
                    replaces.append(replace.strip()) 
                company_replaces.append(replaces)

        context['company_categories'] = company_categories
        context['company_replaces'] = company_replaces

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
