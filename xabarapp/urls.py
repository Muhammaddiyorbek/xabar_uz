from django.urls import path
from .views import *


urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('news/', new_list,name='news_all'),
    path('cantact/', ContactPageView.as_view(),name='cantag_page'),
    path('news/<slug:news>', news_detail,name='new_detail'),
    path('mahaliy/',MahalliyNewsView.as_view(),name='mahaliy'),
    path('xorij/',XorijNewsView.as_view(),name='xorij'),
    path('sport/',SportNewsView.as_view(),name='sport'),
    path('texnalogiya/',TexnalogiyaNewsView.as_view(),name='texnalogiya'),
]