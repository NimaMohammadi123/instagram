from django import forms
from .models import MyUser

class EditForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['photo' , 'first_name' , 'last_name' , 'bio']