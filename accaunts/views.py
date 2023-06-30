from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView,View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import *
from .models import Profile

# Create your views here.
def user_login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(request,
                              username=data['username'],
                              password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Muoffaqyatli login amalga oshirildi!')
                else:
                    return HttpResponse('Sizning profilingiz faol holatda emas!')
            else:
                return HttpResponse('Login va parolda xatolik bor!')
    else:
        form=LoginForm()
    context={
        'form':form
    }
    return render(request,'registration/login.html',context)

@login_required(login_url='login')
def dashboard_view(request):
    user=request.user
    profile_info=Profile.objects.get(user=user)
    print(profile_info)
    context={
        'user':user,
        'profile':profile_info
    }
    return render(request,'pages/user_profile.html',context)

def user_regster_view(request):
    if request.method=="POST":
        user_form=UserRegstrForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            print(new_user)
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,'registration/register_done.html',{'form': user_form})
    else:
        user_form=UserRegstrForm()
    return render(request,'registration/register.html',{'form': user_form})

# class SignupView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/register.html'


@login_required(login_url='login')
def edit_user(request):
    if request.method=='POST':
        user_form=UsrEditForm(instance=request.user,data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form=UsrEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)

    return render(request,'registration/profile_edit.html',{'user_form':user_form,'profile_form':profile_form})



class EditUserView(LoginRequiredMixin,View):
    def get(self,request):
        user_form = UsrEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'registration/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UsrEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')


