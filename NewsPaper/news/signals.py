from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Post


@receiver(pre_save, sender=Post)
def check_post_limit(sender, instance, **kwargs):
    if not instance.pk:
        today = timezone.now().date()
        post_count = Post.objects.filter(
            author=instance.author,
            created_at__date=today
        ).count()

        if post_count >= 3:
            raise ValidationError("Вы не можете публиковать более 3 новостей/статей в сутки.")


@receiver(post_save, sender=Post)
def send_post_notifications(sender, instance, created, **kwargs):
    if created:
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string
        from django.urls import reverse

        for category in instance.categories.all():
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                post_url = reverse('news_detail', args=[str(instance.id)])
                full_url = f"http://{instance._meta.model._meta.site.domain}{post_url}"

                html_content = render_to_string(
                    'newsletter.html',
                    {
                        'post': instance,
                        'user': subscriber,
                        'link': full_url,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f"Новая публикация в категории {category.name}: {instance.title}",
                    body=instance.short_preview(),
                    from_email='oksana.oksanova.80@mail.ru',
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()