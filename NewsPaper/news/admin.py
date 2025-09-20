from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('display_title', 'display_author', 'display_created_at', 'display_rating', 'display_categories')
    list_filter = ('author', 'created_at', 'categories', 'rating')
    search_fields = ('title', 'content')


    def display_title(self, obj):
        return obj.title
    display_title.short_description = 'Заголовок'


    def display_author(self, obj):
        return obj.author
    display_author.short_description = 'Автор'


    def display_created_at(self, obj):
        return obj.created_at
    display_created_at.short_description = 'Создано'


    def display_rating(self, obj):
        return obj.rating
    display_rating.short_description = 'Рейтинг'


    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'Категории'



class CommentAdmin(admin.ModelAdmin):
    list_display = ('display_title', 'display_comment', 'display_user', 'display_created_at', 'display_rating')
    list_filter = ('user__username', 'created_at', 'rating')
    search_fields = ('text', 'post__title')


    def display_title(self, obj):
        return obj.post.title
    display_title.short_description = 'Заголовок'


    def display_comment(self, obj):
        return obj.text
    display_comment.short_description = 'Комментарий'


    def display_user(self, obj):
        return obj.user
    display_user.short_description = 'Пользователь'


    def display_created_at(self, obj):
        return obj.created_at
    display_created_at.short_description = 'Создано'


    def display_rating(self, obj):
        return obj.rating
    display_rating.short_description = 'Рейтинг'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('display_user', 'display_first_name', 'display_last_name', 'display_rating')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def display_user(self, obj):
        return obj.user
    display_user.short_description = 'Пользователь'


    def display_first_name(self, obj):
        return obj.user.first_name
    display_first_name.short_description = 'Имя'


    def display_last_name(self, obj):
        return obj.user.last_name
    display_last_name.short_description = 'Фамилия'


    def display_rating(self, obj):
        return obj.rating
    display_rating.short_description = 'Рейтинг'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'subscribers_count')
    search_fields = ('name',)

    def display_name(self, obj):
        return obj.name
    display_name.short_description = 'Категория'

    def subscribers_count(self, obj):
        return obj.subscribers.count()
    subscribers_count.short_description = 'Подписчиков'


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
admin.site.unregister(PostCategory)