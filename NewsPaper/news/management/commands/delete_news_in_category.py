from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляются все новости в выбранной категории'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str, help='Название категории для удаления постов')


    def handle(self, *args, **options):
        category_name = options['category']

        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Категория "{category_name}" не найдена'))
            return

        self.stdout.write(f'Вы действительно хотите удалить все посты в категории "{category_name}"? yes/no')
        answer = input().strip().lower()

        if answer == 'yes':
            count, _ = Post.objects.filter(categories=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Успешно удалено {count} постов в категории "{category_name}"!'))
        else:
            self.stdout.write(self.style.ERROR('Операция отменена'))