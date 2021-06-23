from django import forms
from .models import Post
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'body')

        widgets = {
            # bootstrap 'form-control' class
            'title': forms.TextInput(attrs={'class': 'border-purple rounded-0 mb-2'}),
            # 'author': User,     try to make it so that the current sesion user is the author!!
            'author': forms.Select(attrs={'class': 'border-purple rounded-0 mb-2'}),
            'body': forms.Textarea(attrs={'class': 'border-purple rounded-0 mb-2'}),
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')

        widgets = {
            # bootstrap 'form-control' class
            'title': forms.TextInput(attrs={'class': 'border-purple rounded-0 mb-2'}),
            # 'author': forms.Select(attrs={'class': 'border-purple rounded-0 mb-2'}),
            'body': forms.Textarea(attrs={'class': 'border-purple rounded-0 mb-2'}),
        }
