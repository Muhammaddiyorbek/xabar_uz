from django import forms
from .models import *



class CantactForms(forms.ModelForm):
    class Meta:
        model=Contact
        fields="__all__"
