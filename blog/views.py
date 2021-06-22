from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# def blog(request):
#     return render(request, 'blog/blog.html', {})

class BlogView(ListView):
    model = Post
    template_name = 'blog/blog.html'


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'blog/article_details.html'
