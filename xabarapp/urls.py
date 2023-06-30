from django.urls import path
from .views import *

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('super/admin/',admin_panel,name='admin_panel'),
    path('news/', new_list,name='news_all'),
    path('search/',SearchResoult.as_view(),name='search'),
    path('catigory/create/', CatigoryCreateView.as_view(),name='catigory_create'),
    path('news/create/', NewsCreateView.as_view(),name='news_create'),
    path('cantact/', ContactPageView.as_view(),name='cantag_page'),
    path('news/<slug:news>', news_detail,name='new_detail'),
    path('news/edit/<slug>',NewsUpdateView.as_view(),name='new_edit'),
    path('news/delete/<slug>',NewsDeleteView.as_view(),name='new_delete'),
    path('mahaliy/',MahalliyNewsView.as_view(),name='mahaliy'),
    path('xorij/',XorijNewsView.as_view(),name='xorij'),
    path('sport/',SportNewsView.as_view(),name='sport'),
    path('texnalogiya/',TexnalogiyaNewsView.as_view(),name='texnalogiya'),
]


