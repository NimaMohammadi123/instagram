from django import forms
from myuser.models import MyUser
from django.core.validators import MaxValueValidator , MinValueValidator


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password' , widget=forms.PasswordInput)
    password2 = forms.CharField(label='password confirm' , widget= forms.PasswordInput)
    
    class Meta:
        model = MyUser
        fields =['phone','username','email']


class VerifyForm(forms.Form):
    code = forms.IntegerField(validators=[MinValueValidator(11111) , MaxValueValidator(99999)])