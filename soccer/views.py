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
from . import serializers
from .forms import ContactForm, FilesForm, ContactFormSet

import requests
from bs4 import BeautifulSoup


# Create your views here.
logger = logging.getLogger(__name__)

# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/



class IndexPageView(TemplateView):
    template_name = "soccer/index2.html"

    def get_league_data(self):
        rows = []
        url = 'https://www.premierleague.com/stats/top/players'
        s = requests.Session()

        req = s.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        #logger.info(soup.find_all('section', {'class':'mainWidget'}))
        for i, e in enumerate(soup.find_all('ul', {'class':'statsList'})):
            #logger.info(e.previous_sibling.get_text())
            rows.append(e.previous_sibling.get_text())
            l = []
            rd = e.find('li', {'class':'statsHero'})
            l.append(rd.find('div', {'class':'pos'}).text)
            l.append(rd.find('a', {'class':'statName'}).text)
            l.append(rd.find('a', {'class':'statNameSecondary'}).text)
            l.append(rd.find('div', {'class':'stat'}).text)
            
            #logger.info(",".join(l))
            rows.append(",".join(l))

            for r in e.find_all('li', {'class':'statsRow'}):
                l = []
                l.append(r.find('div', {'class':'pos'}).text)
                l.append(r.find('a', {'class':'statName'}).text)
                l.append(r.find('a', {'class':'statNameSecondary'}).text)
                l.append(r.find('div', {'class':'stat'}).text)
                #logger.info(",".join(l))
                rows.append(",".join(l))
            #logger.info("")

            #else:
            #    logger.info(e.find_all('li', {'class':'statsRow'}))
        return rows

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['leagues'] = models.Leagues.objects.all()
        context['teams'] = models.Teams.objects.filter(ranking__isnull=False).order_by('ranking')
        context['matchs'] = models.Matchs.objects.order_by('-date')[:5]
        #rankings = self.get_league_data()
        
        return context

class NewIndexPageView(TemplateView):
    #<!--<td>{{next_matchs|index:forloop.counter0}}</td>-->
    template_name = "soccer/list.html"

    def get_context_data(self, **kwargs):
        import datetime
        context = super(NewIndexPageView, self).get_context_data(**kwargs)
        # filter by Korea team 
        #__korea = models.Teams.objects.get(name='한국')
        #context['matchs'] = models.Matchs.objects.filter(Q(home=__korea) | Q(away=__korea)).order_by('-date')
        

        __k_league = models.Leagues.objects.get(name='KOR D1')
        matchs = models.Matchs.objects.filter(Q(league=__k_league)).order_by('-date')
        next_matchs = []
        ing_matchs = []
        before_matchs = []

        #TODO:the match status need to be add in model or update status
        # status field <- get data from server via ajax,,,, etc

        for match in matchs:
            date_diff = datetime.datetime.strptime(match.date, '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()
            if date_diff > datetime.timedelta(0,7200):
                next_matchs.append(match)
            elif date_diff < datetime.timedelta(0,7200) and date_diff >= datetime.timedelta(0,0):
                ing_matchs.append(match)
            else:
                before_matchs.append(match)

        context['next_matchs'] = next_matchs
        context['ing_matchs'] = ing_matchs
        context['before_matchs'] = before_matchs
        #for i, e in enumerate(soup.find_all('ul', {'class':'statsList'})):

        for lmatch in matchs:
            try:
                predict = models.MatchPredictVariables.objects.get(match=lmatch)
                if float(predict.h_x1) > 0.0:
                    A = 0.4
                    B = 0.3
                    C = 0.2
                    D = 0.1

                    print (lmatch, lmatch.hscore, lmatch.ascore)
                    print ((predict.h_x1*A + predict.h_x2*B + predict.h_x3*C + predict.h_x4*D)*100)
                    print ((predict.a_x1*A + predict.a_x2*B + predict.a_x3*C + predict.a_x4*D)*100)
                    print (predict.h_x1,predict.h_x2, predict.h_x3, predict.h_x4)
                    print (predict.a_x1,predict.a_x2, predict.a_x3, predict.a_x4)
                    print ("---------------------------------------------------------------------")
                '''
                print ("%s, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f" % (predict.match, predict.h_x1, predict.h_x2, predict.h_x3,
                    predict.h_x4, predict.h_x5, predict.h_x6, predict.a_x1, predict.a_x2,
                    predict.a_x3, predict.a_x4, predict.a_x5, predict.a_x6))
                '''
                #a  : odd       - x1
                #b  : recent    - x2 
                #c  : history   - x3
                #d  : draw      - x4


                #winnner define 
            except Exception as E:
                pass
        
        #Order by date : 5 items
        #context['matchs'] = models.Matchs.objects.all()#order_by('-date')[:5]
        
        return context
        

class TimeLinePageView(TemplateView):
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

class DetailPageView(TemplateView):
    template_name = "soccer/detail.html"

    def get_context_data(self, **kwargs):
        context = super(DetailPageView, self).get_context_data(**kwargs)
        code = context['match_id']
        _a = models.Matchs.objects.get(code=code)
        logger.debug(_a)
        context['info'] = _a
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



# 한글!!
#===========================================================================================
rowsPerPage = 2    
 

def home(request):   
    #OK
    #url = '/listSpecificPageWork?current_page=1' 
    #return HttpResponseRedirect(url)  

    boardList = FreeBoard.objects.order_by('-id')[0:2]        
    current_page =1
    totalCnt = FreeBoard.objects.all().count() 
    
    pagingHelperIns = pagingHelper();
    totalPageList = pagingHelperIns.getTotalPageList( totalCnt, rowsPerPage)
    logger.info(totalPageList)
    
    return render_to_response('board/listSpecificPage.html', {'boardList': boardList, 'totalCnt': totalCnt, 
                                                        'current_page':current_page ,'totalPageList':totalPageList} ) 
    
#===========================================================================================
def show_write_form(request):
    return render_to_response('board/writeBoard.html')  

#===========================================================================================
@csrf_exempt
def DoWriteBoard(request):
    logger.info(request.POST)
    br = FreeBoard (subject = request.POST['subject'],
                      name = request.POST['name'],
                      mail = request.POST['email'],
                      memo = request.POST['memo'],
                      created_date = timezone.now(),
                      hits = 0
                     )
    br.save()
    
    # 다시 조회    
    url = 'board/listSpecificPageWork?current_page=1' 
    return HttpResponseRedirect(url)    
                   

#===========================================================================================
def viewWork(request):
    pk= request.GET['memo_id']    
    #print 'pk='+ pk
    boardData = FreeBoard.objects.get(id=pk)
    #print boardData.memo
    
    # Update DataBase
    logger.info( 'boardData.hits', boardData.hits)
    FreeBoard.objects.filter(id=pk).update(hits = boardData.hits + 1)
      
    return render_to_response('board/viewMemo.html', {'memo_id': request.GET['memo_id'], 
                                                'current_page':request.GET['current_page'], 
                                                'searchStr': request.GET['searchStr'], 
                                                'boardData': boardData } )            
   
#===========================================================================================
def listSpecificPageWork(request):    
    current_page = request.GET['current_page']
    totalCnt = FreeBoard.objects.all().count()                  
    
    logger.info( 'current_page=', current_page)
        
    # 페이지를 가지고 범위 데이터를 조회한다 => raw SQL 사용함
    boardList = FreeBoard.objects.raw('SELECT Z.* FROM(SELECT X.*, ceil( rownum / %s ) as page FROM ( SELECT ID,SUBJECT,NAME, CREATED_DATE, MAIL,MEMO,HITS \
                                        FROM SAMPLE_BOARD_FreeBoard  ORDER BY ID DESC ) X ) Z WHERE page = %s', [rowsPerPage, current_page])
        
    logger.info(  'boardList=',boardList, 'count()=', totalCnt)
    
    # 전체 페이지를 구해서 전달...
    pagingHelperIns = pagingHelper();
    
    totalPageList = pagingHelperIns.getTotalPageList( totalCnt, rowsPerPage)
        
    logger.info( 'totalPageList', totalPageList)
    
    return render_to_response('board/listSpecificPage.html', {'boardList': boardList, 'totalCnt': totalCnt, 
                                                        'current_page':int(current_page) ,'totalPageList':totalPageList} )

#===========================================================================================

def listSpecificPageWork_to_update(request):
    memo_id = request.GET['memo_id']
    current_page = request.GET['current_page']
    searchStr = request.GET['searchStr']
    
    #totalCnt = FreeBoard.objects.all().count()
    logger.info( 'memo_id', memo_id)
    logger.info( 'current_page', current_page)
    logger.info( 'searchStr', searchStr)
    
    boardData = FreeBoard.objects.get(id=memo_id)
      
    return render_to_response('board/viewForUpdate.html', {'memo_id': request.GET['memo_id'], 
                                                'current_page':request.GET['current_page'], 
                                                'searchStr': request.GET['searchStr'], 
                                                'boardData': boardData } )    

#===========================================================================================
@csrf_exempt
def updateBoard(request):
    memo_id = request.POST['memo_id']
    current_page = request.POST['current_page']
    searchStr = request.POST['searchStr']        
        
    logger.info( '#### updateBoard ######')
    logger.info( 'memo_id', memo_id)
    logger.info( 'current_page', current_page)
    logger.info( 'searchStr', searchStr)
    
    # Update DataBase
    FreeBoard.objects.filter(id=memo_id).update(
                                                  mail= request.POST['mail'],
                                                  subject= request.POST['subject'],
                                                  memo= request.POST['memo']
                                                  )
    
    # Display Page => POST 요청은 redirection!
    url = 'board/listSpecificPageWork?current_page=' + str(current_page)
    return HttpResponseRedirect(url)    
      

#===========================================================================================
def DeleteSpecificRow(request):
    memo_id = request.GET['memo_id']
    current_page = request.GET['current_page']
    logger.info( '#### DeleteSpecificRow ######')
    logger.info( 'memo_id', memo_id)
    logger.info( 'current_page', current_page)
    
    p = FreeBoard.objects.get(id=memo_id)
    p.delete()
    
    # Display Page    
    # 마지막 메모를 삭제하는 경우, 페이지를 하나 줄임.
    totalCnt = FreeBoard.objects.all().count()  
    pagingHelperIns = pagingHelper();
    
    totalPageList = pagingHelperIns.getTotalPageList( totalCnt, rowsPerPage)
    logger.info( 'totalPages', totalPageList)
    
    if( int(current_page) in totalPageList):
        logger.info( 'current_page No Change')
        current_page=current_page
    else:
        current_page= int(current_page)-1
        logger.info( 'current_page--'            )
            
    url = 'board//listSpecificPageWork?current_page=' + str(current_page)
    return HttpResponseRedirect(url)    

#===========================================================================================
@csrf_exempt
def searchWithSubject(request):
    searchStr = request.POST['searchStr']
    logger.info( 'searchStr', searchStr)
    
    url = 'board/listSearchedSpecificPageWork?searchStr=' + searchStr +'&pageForView=1'
    return HttpResponseRedirect(url)    
         
        
#===========================================================================================    
def listSearchedSpecificPageWork(request):
    searchStr = request.GET['searchStr']
    pageForView = request.GET['pageForView']
    logger.info( 'listSearchedSpecificPageWork:searchStr', searchStr, 'pageForView=', pageForView)
        
    #boardList = FreeBoard.objects.filter(subject__contains=searchStr)
    #print  'boardList=',boardList
    
    totalCnt = FreeBoard.objects.filter(subject__contains=searchStr).count()
    logger.info(  'totalCnt=',totalCnt)
    
    pagingHelperIns = pagingHelper();
    totalPageList = pagingHelperIns.getTotalPageList( totalCnt, rowsPerPage)
    
    # like 구문 적용방법 
    boardList = FreeBoard.objects.raw("""SELECT Z.* FROM ( SELECT X.*, ceil(rownum / %s) as page \
        FROM ( SELECT ID,SUBJECT,NAME, CREATED_DATE, MAIL,MEMO,HITS FROM SAMPLE_BOARD_FreeBoard \
        WHERE SUBJECT LIKE '%%'||%s||'%%' ORDER BY ID DESC) X ) Z WHERE page = %s""", [rowsPerPage, searchStr, pageForView])
        
    logger.info('boardList=',boardList)
    
    return render_to_response('board/listSearchedSpecificPage.html', {'boardList': boardList, 'totalCnt': totalCnt, 
                                                        'pageForView':int(pageForView) ,'searchStr':searchStr, 'totalPageList':totalPageList} )            
    
#===========================================================================================
