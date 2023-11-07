from django import forms
from .models import *
from django.core.files.storage import FileSystemStorage

doc = FileSystemStorage(location='/media/documents')
                       
class LoginForm(forms.Form):
    Login = forms.CharField(max_length=50,widget=forms.TextInput(attrs=({'class':'input100','type':'text','name':'Login'})))
    Password = forms.CharField(max_length=255,widget=forms.TextInput(attrs=({'class':'input100','type':'password','name':'Password'})))

class RegisterForm(forms.Form):
    Login = forms.CharField(max_length=50,widget=forms.TextInput(attrs=({'class':'input100','type':'text','name':'Login'})))
    Password = forms.CharField(max_length=255,widget=forms.TextInput(attrs=({'class':'input100','type':'password','name':'Password'})))
    ConfirmPassword = forms.CharField(max_length=255,widget=forms.TextInput(attrs=({'class':'input100','type':'password','name':'ConfirmPassword'})))

class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('name', 'document')
        widgets = {
            "name": forms.TextInput(attrs=({'class':'input100'})),
        }

class TOTPConfirmForm(forms.Form):
    Code = forms.CharField(max_length=6)
    