from django.shortcuts import render,get_object_or_404
from .models import *
from .forms import *
from django.http import HttpResponse
from django.views.generic import *


# def indexview(request):
#     new_lis=News.objects.all().order_by('-publish_time')[:5]
#     catigor_lis=Catigor.objects.all()
#     mahalliy_news=News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[1:6]
#     mahalliy_one=News.published.filter(category__name='Mahalliy').order_by('-publish_time')[0]
#     context={
#         'new_lis':new_lis,
#         'catigor_lis':catigor_lis,
#         'mahalliy':mahalliy_news,
#         'mahalliy_one':mahalliy_one
#     }
#     return render(request,'index.html',context)

class HomePageView(ListView):
    model=News
    template_name='index.html'
    context_object_name='new_lis'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['catigor_lis']=Catigor.objects.all()
        context['new_lis']=News.objects.all().order_by('-publish_time')[:5]
        context['mahalliy']=News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[:6]
        context['xorij_xabarlari']=News.published.all().filter(category__name='Xorij').order_by('-publish_time')[:6]
        context['sport_xabarlari']=News.published.all().filter(category__name='Sport').order_by('-publish_time')[:6]
        context['texnalogiya_xabarlari']=News.published.all().filter(category__name='Texnalogiya').order_by('-publish_time')[:6]
        

        return context

def new_list(request):
    news_all=News.objects.all()
    context={
        'news_list':news_all
    }
    return render(request,'news_list.html',context)

def news_detail(request,news):
    new_detail=get_object_or_404(News, slug=news)
    context={
        'new_detail':new_detail
    }
    return render(request,'news_detail.html',context)

# def contactPage(request):
#     form=CantactForms(request.POST or None)
#     if request.method=="POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h1>Malumotlar to'g'ri biz bilan bog'langaningiz uchun tashakkur!</h1>")
#     context={
#         'form':form
#     }
#     return render(request,'contact.html',context)

class ContactPageView(TemplateView):
    template_name='contact.html'

    def get(self,request,*args,**kwargs):
        form=CantactForms()
        context={
            'form':form
        }
        return render(request,'contact.html',context)
    
    def post(self,request,*args,**kwargs):
        form=CantactForms(request.POST)
        if request.method=='POST' and form.is_valid():
            form.save()
            return HttpResponse("<h1>Malumotlar to'g'ri biz bilan bog'langaningiz uchun tashakkur!</h1>")

        context={
            'form':form
        }
        return render(request,'contact.html',context)
    
class MahalliyNewsView(ListView):
    model=News
    template_name='mahalliy.html'
    context_object_name='mahaliy_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Mahalliy')
        return news
    
class XorijNewsView(ListView):
    model=News
    template_name='xorij.html'
    context_object_name='xorij_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Xorij')
        return news

class TexnalogiyaNewsView(ListView):
    model=News
    template_name='texnalogiya.html'
    context_object_name='texnalogiya_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Texnalogiya')
        return news

class SportNewsView(ListView):
    model=News
    template_name='sport.html'
    context_object_name='sport_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Sport')
        return news