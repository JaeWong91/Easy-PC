from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm, EditForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages


class BlogView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    ordering = ['-id']
    

class ArticleDetailView(DetailView):
    model = Post
    template_name = 'blog/article_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()

        blog_id = get_object_or_404(Post, id=self.kwargs['pk'])   # grab from post table the id of the Post we are currently on
        total_likes = blog_id.total_likes()

        liked = False
        if blog_id.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'
    # fields = '__all__'
    # fields = ('title', 'body')


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'blog/edit_post.html'
    # fields = ['title', 'body']


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog')


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))      # 'post_id' is the name of the Like button we assigned, lookup from the Post table

    if request.user.is_authenticated:
        liked = False
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)     # when user unliked post, Liked = False
            liked = False
            messages.success(request, 'Sorry to hear that you disliked this post!')
            return HttpResponseRedirect(reverse('article_detail',
                                                args=[str(pk)]))
        else:
            post.likes.add(request.user)
            liked = True
            messages.success(request, 'You liked this post!')
            return HttpResponseRedirect(reverse('article_detail',
                                                args=[str(pk)]))
    else:
        messages.error(request, 'You must be logged in to like an article!')
        return HttpResponseRedirect(reverse('article_detail', args=[str(pk)]))
