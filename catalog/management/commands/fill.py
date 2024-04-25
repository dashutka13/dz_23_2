from django.core.management import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):

        Category.objects.all().delete()
        Product.objects.all().delete()

        cat_1 = Category.objects.create(name='Обычный', pk=6)
        cat_2 = Category.objects.create(name='Волшебный', pk=7)

        Product.objects.create(name='Пи́джи', category=cat_1, unit_price=5000, date_of_creation='2023-11-14', last_modified_date='2023-11-14')
        Product.objects.create(name='Клефе́йбл', category=cat_2, unit_price=3200, date_of_creation='2023-11-14', last_modified_date='2023-11-14')
