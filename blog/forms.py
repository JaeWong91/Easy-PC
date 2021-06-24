from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'body', 'snippet', 'header_image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'border-purple rounded-0 mb-2'}),
            'author': forms.TextInput(attrs={'class': 'border-purple rounded-0 mb-2', 'value': '', 'id': 'elder', 'type': 'hidden'}),
            'body': forms.Textarea(attrs={'class': 'border-purple rounded-0 mb-2'}),
            'snippet': forms.Textarea(attrs={'class': 'border-purple rounded-0 mb-2'}),
            
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'snippet', 'header_image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'border-purple rounded-0 mb-2'}),
            'author': forms.Select(attrs={'class': 'border-purple rounded-0 mb-2'}),
            'body': forms.Textarea(attrs={'class': 'border-purple rounded-0 mb-2'}),
            'snippet': forms.Textarea(attrs={'class': 'border-purple rounded-0 mb-2'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'border-purple rounded-0 mb-2'}),
            'body': forms.Textarea(attrs={'class': 'border-purple rounded-0 mb-2'}),
            
        }
