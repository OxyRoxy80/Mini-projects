import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.tasks import send_weekly_newsletter_task

logger = logging.getLogger(__name__)

def trigger_weekly_newsletter():
    try:
        result = send_weekly_newsletter_task.delay()
        logger.info(f"Задача еженедельной рассылки поставлена в очередь Celery: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Ошибка при постановке задачи в Celery: {e}")
        return None

def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler for weekly newsletter with Celery integration"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            trigger_weekly_newsletter,
            trigger=CronTrigger(day_of_week="mon", hour="8", minute="00"),
            id="weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_newsletter' with Celery integration.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler with Celery integration...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")