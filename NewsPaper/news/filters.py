import django_filters
from django import forms
from .models import Post, Author


class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='iregex',
        label='Название',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    author = django_filters.ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Все авторы',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    created_at = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='Дата (не ранее)',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    class Meta:
        model = Post
        fields = ['title', 'author', 'created_at']
