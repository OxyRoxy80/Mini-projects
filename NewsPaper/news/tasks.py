from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from .models import Post, Category
from django.utils import timezone
from datetime import timedelta
import logging


@shared_task
def send_post_notifications_task(post_id):
    try:
        post = Post.objects.get(id=post_id)

        for category in post.categories.all():
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                post_url = reverse('news_detail', args=[str(post.id)])
                full_url = f"http://127.0.0.1:8000{post_url}"

                html_content = render_to_string(
                    'newsletter.html',
                    {
                        'post': post,
                        'user': subscriber,
                        'link': full_url,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f"Новая публикация в категории {category.name}: {post.title}",
                    body=post.short_preview(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

        print(f"Уведомления отправлены для поста {post.title}")

    except Post.DoesNotExist:
        print(f"Пост с ID {post_id} не найден")
    except Exception as e:
        print(f"Ошибка при отправке уведомлений: {e}")


logger = logging.getLogger(__name__)


@shared_task
def send_weekly_newsletter_task():
    one_week_ago = timezone.now() - timedelta(weeks=1)

    total_emails_sent = 0
    total_errors = 0

    for category in Category.objects.all():
        new_posts = Post.objects.filter(
            categories=category,
            created_at__gte=one_week_ago,
            created_at__lte=timezone.now()
        ).order_by('-created_at')

        if new_posts.exists() and category.subscribers.exists():
            subscribers = category.subscribers.all()

            for subscriber in subscribers:
                try:
                    html_content = render_to_string(
                        'weekly_newsletter.html',
                        {
                            'category': category,
                            'posts': new_posts,
                            'user': subscriber,
                            'week_start': one_week_ago.date(),
                            'week_end': timezone.now().date(),
                        }
                    )

                    msg = EmailMultiAlternatives(
                        subject=f"Новые статьи в категории '{category.name}'",
                        body=f"За неделю: {new_posts.count()} новых статей",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[subscriber.email],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    total_emails_sent += 1
                    logger.info(f"Рассылка отправлена для {subscriber.email}")

                except Exception as e:
                    total_errors += 1
                    logger.error(f"Ошибка при отправке для {subscriber.email}: {e}")

    logger.info(f"Еженедельная рассылка завершена. Отправлено: {total_emails_sent}, ошибок: {total_errors}")
    return {'emails_sent': total_emails_sent, 'errors': total_errors}

