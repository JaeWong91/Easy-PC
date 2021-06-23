from django.urls import path
# from . import views
from .views import (BlogView, ArticleDetailView,
                    AddPostView, UpdatePostView, DeletePostView)

urlpatterns = [
    #path('', views.blog, name='blog'),
    path('', BlogView.as_view(), name='blog'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name='edit_post'),
    path('article/<int:pk>/remove', DeletePostView.as_view(), name='delete_post'),
]
