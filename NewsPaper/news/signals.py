from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Post, PostCategory
from .tasks import send_post_notifications_task


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


@receiver(m2m_changed, sender=Post.categories.through)
def send_post_notifications(sender, instance, action, **kwargs):
    if action == 'post_add':
        send_post_notifications_task.delay(instance.id)
