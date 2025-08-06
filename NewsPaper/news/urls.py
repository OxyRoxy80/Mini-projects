from django.urls import path
from .views import (
    NewsList, NewsDetail, NewsCreate, ArticlesCreate, NewsUpdate, ArticlesUpdate,
    NewsDelete, ArticlesDelete, subscribe, unsubscribe,
)

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='news_delete'),
    path('category/<int:category_id>/subscribe/', subscribe, name='subscribe'),
    path('category/<int:category_id>/unsubscribe/', unsubscribe, name='unsubscribe'),
]
