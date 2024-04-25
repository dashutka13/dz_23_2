from django.contrib.auth import get_user_model
from django.db import models


# Объявление словаря NULLABLE
NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='категория')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(verbose_name='превью', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit_price = models.IntegerField(verbose_name='цена за единицу товара')
    date_of_creation = models.DateField(verbose_name='дата создания')
    last_modified_date = models.DateField(verbose_name='дата последнего изменения')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, **NULLABLE, verbose_name='владелец')
    is_published = models.BooleanField(default=False, verbose_name='признак публикации')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name',)


class Blog(models.Model):
    blog_title = models.CharField(max_length=50, verbose_name='заголовок')
    preview = models.ImageField(verbose_name='превью', **NULLABLE)
    body = models.TextField(verbose_name='содержимое')
    date_of_creation = models.DateField(verbose_name='дата создания')

    slug = models.CharField(max_length=150, verbose_name="slug", null=True, blank=True)
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.blog_title} {self.preview}'

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'
        ordering = ('blog_title',)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    num = models.IntegerField(verbose_name='номер версии')
    name = models.CharField(max_length=50, verbose_name='название версии')
    is_active = models.BooleanField(default=False, verbose_name='признак текущей версии')

    def __str__(self):
        return f'{self.product.name} version:{self.num}-{self.is_active}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
        ordering = ('name',)

