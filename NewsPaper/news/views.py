from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from .models import Post
from .filters import NewsFilter
from .forms import NewsForm


class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'news1.html'
    context_object_name = 'news1'

class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        return super().form_valid(form)

class ArticlesCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)

class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        return super().form_valid(form)


class ArticlesUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
