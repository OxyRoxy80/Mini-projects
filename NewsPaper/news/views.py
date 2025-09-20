from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from .models import Post, Category
from .filters import NewsFilter
from .forms import NewsForm
from django.core.cache import cache


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
        context['categories'] = Category.objects.all()
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'news1.html'
    context_object_name = 'news1'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        post.save()
        form.save_m2m()
        return super().form_valid(form)

class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        post.save()
        form.save_m2m()
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    login_url = reverse_lazy('account_login')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        return super().form_valid(form)

class ArticlesUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    login_url = reverse_lazy('account_login')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)

class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    login_url = reverse_lazy('account_login')

class ArticlesDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    login_url = reverse_lazy('account_login')


@login_required
def subscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    return redirect('news_list')


@login_required
def unsubscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.remove(request.user)
    return redirect('news_list')