"""playground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

from soccer import views as soccer_views
from comingsoon import views as comingsoon_views
from nojapan import views as nojapan_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'', include('chat.urls', namespace='chat')),
    #url(r'', include('chat.urls', namespace='chat')),
    #url(r'^$', comingsoon_views.IndexPageView.as_view(), name="coming_soon"),
    #url(r'^$', nojapan_views.NoJapanIdexPageView.as_view(), name="nojapn"),
    #url(r'^$', views.HomePageView.as_view(), name="home"),
    #url(r"^formset$", views.DefaultFormsetView.as_view(), name="formset_default"),
    #url(r"^form$", views.DefaultFormView.as_view(), name="form_default"),
    #url(r"^form_by_field$", views.DefaultFormByFieldView.as_view(), name="form_by_field"),
    #url(r"^form_horizontal$", views.FormHorizontalView.as_view(), name="form_horizontal"),
    #url(r"^form_inline$", views.FormInlineView.as_view(), name="form_inline"),
    #url(r"^form_with_files$", views.FormWithFilesView.as_view(), name="form_with_files"),
    #url(r"^pagination$", views.PaginationView.as_view(), name="pagination"),
    #url(r"^misc$", views.MiscView.as_view(), name="misc"),

    url(r'^$', nojapan_views.NoJapanIdexPageView.as_view(), name="nojapn"),
    url(r'nojapan/', include('nojapan.urls', namespace='nojapan')),
    url(r'soccer/', include('soccer.urls', namespace='soccer')),
    url(r'^goaccess/', include('goaccess.urls', namespace='goaccess')),
    #url(r'^playground/soccer/', include('soccer.urls', namespace='soccer')),
]
