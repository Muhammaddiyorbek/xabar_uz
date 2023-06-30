from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username=forms.CharField(max_length=250)
    password=forms.CharField(widget=forms.PasswordInput)

class UserRegstrForm(forms.ModelForm):
    password=forms.CharField(label='Parol',widget=forms.PasswordInput)
    password2=forms.CharField(label='Parolni takrorlang',widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','first_name','email','last_name']
    def clean_password2(self):
        data=self.cleaned_data
        if data['password']!=data['password2']:
            raise forms.ValidationError('Ikkala parol ham bir-hil bolishi kerak!')
        return data['password2']

class UsrEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['date_of_birth','photo']