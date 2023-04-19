from email.policy import default
from pyexpat import model
from django import forms
from .models import Post , PostComment

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image' , 'caption']

class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['text']

