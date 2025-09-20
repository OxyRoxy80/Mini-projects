from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = self.post_set.aggregate(pr=Sum('rating'))['pr'] or 0
        comment_rating = self.user.comment_set.aggregate(cr=Sum('rating'))['cr'] or 0
        post_comments_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Sum('rating'))['pcr'] or 0

        self.rating = post_rating * 3 + comment_rating + post_comments_rating
        self.save()

    def __str__(self):
        return f'{self.user.get_full_name()}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=NEWS)
    created_at = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length=128)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content

    def short_preview(self):
        return self.content[:50] + '...' if len(self.content) > 50 else self.content

    def __str__(self):
        return f'{self.title}: {self.content[:20]}...'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    class Meta:
        unique_together = ('post', 'category')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.user.get_full_name()}: {self.text[:30]}...'
