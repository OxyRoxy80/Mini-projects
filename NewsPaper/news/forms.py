from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError
from django.utils import timezone


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'content',
            'categories',
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'category-checkboxes'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),

        }
        labels = {
            'categories': 'Категории',
            'author': 'Автор',
            'title': 'Название',
            'content': 'Контент',
        }
