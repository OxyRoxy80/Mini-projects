# from django.shortcuts import render
# from django.template.defaultfilters import title
from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post

class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'news'



class NewsDetail(DetailView):
    model = Post
    template_name = 'news1.html'
    context_object_name = 'news1'