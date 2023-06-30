from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render,get_object_or_404
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.http import HttpResponse
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from xabaruz.custom_permison import OnlyLoggedSuperUser



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

@login_required(login_url='login')
def new_list(request):
    news_all=News.objects.all()
    context={
        'news_list':news_all
    }
    return render(request,'news_list.html',context)

@login_required(login_url='login')
def news_detail(request,news):
    new_detail=get_object_or_404(News, slug=news,status=News.Status.Published)
    context={}
    hit_count=get_hitcount_model().objects.get_for_object(new_detail)
    hits=hit_count.hits
    hitcontext=context['hitcount']={'pk':hit_count.pk}
    hitcount_response=HitCountMixin.hit_count(request,hit_count)
    if hitcount_response.hit_counted:
        hits=hits+1
        hitcontext['hit_counted']=hitcount_response.hit_counted
        hitcontext['hit_message']=hitcount_response.hit_message
        hitcontext['total_hits']=hits
    comments=new_detail.comments.filter(active=True)
    comment_count=comments.count()
    new_comment=None
    if request.method=="POST":
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.news=new_detail
            new_comment.user=request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form=CommentForm()
    context={
        'new_detail':new_detail,
        'comments':comments,
        'new_comment':new_comment,
        'comment_count':comment_count,
        'comment_form':comment_form
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

class ContactPageView(LoginRequiredMixin,TemplateView):
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
    
class MahalliyNewsView(LoginRequiredMixin,ListView):
    model=News
    template_name='mahalliy.html'
    context_object_name='mahaliy_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Mahalliy')
        return news
    
class XorijNewsView(LoginRequiredMixin,ListView):
    model=News
    template_name='xorij.html'
    context_object_name='xorij_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Xorij')
        return news

class TexnalogiyaNewsView(LoginRequiredMixin,ListView):
    model=News
    template_name='texnalogiya.html'
    context_object_name='texnalogiya_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Texnalogiya')
        return news

class SportNewsView(LoginRequiredMixin,ListView):
    model=News
    template_name='sport.html'
    context_object_name='sport_yangiliklar'

    def get_queryset(self):
        news=self.model.published.all().filter(category__name='Sport')
        return news
    
class NewsUpdateView(OnlyLoggedSuperUser,UpdateView):
    model=News
    fields=['title','body','image','category','status']
    template_name='news_edit.html'


    

class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
    model=News
    template_name='news_delete.html'
    success_url=reverse_lazy('home')

class CatigoryCreateView(OnlyLoggedSuperUser,CreateView):
    model=Catigor
    template_name='catigory_create.html'
    fields=['name','url']
    success_url = reverse_lazy('home')
class NewsCreateView(OnlyLoggedSuperUser,CreateView):
    model=News
    template_name='news_create.html'
    fields=['title','body','image','category','status']

@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_panel(request):
    admin_users=User.objects.filter(is_superuser=True)
    context={
        'admin_users':admin_users
    }
    return render(request,'pages/admin_panel.html',context)

class SearchResoult(ListView):
    model = News
    template_name = 'search_list.html'
    context_object_name = 'search_list'

    def get_queryset(self):
        query=self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query)|Q(body__icontains=query))