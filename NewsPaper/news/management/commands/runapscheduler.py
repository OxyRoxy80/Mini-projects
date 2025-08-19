import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils import timezone
from datetime import timedelta
from news.models import Category, Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


def send_weekly_newsletter():
    one_week_ago = timezone.now() - timedelta(weeks=1)

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
                        from_email='oksana.oksanova.80@mail.ru',
                        to=[subscriber.email],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    logger.info(f"Рассылка отправлена для {subscriber.email}")

                except Exception as e:
                    logger.error(f"Ошибка: {e}")

def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler for weekly newsletter"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_newsletter,
            trigger=CronTrigger(day_of_week="mon", hour="9", minute="0"),
            id="weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_newsletter'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="0", minute="0"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")