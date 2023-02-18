from django.db import models
from django.urls import reverse
from main.utils import get_product_main_image_path, get_extra_image_path


class Category(models.Model):
    name = models.CharField(max_length=25,
                            verbose_name='Название категории')
    slug = models.SlugField(unique=True, db_index=True, max_length=25,
                            verbose_name='Интернет имя категории(slug)')
    order = models.PositiveSmallIntegerField(default=0,
                                             verbose_name='Порядок сортитовки',
                                             help_text='Установите порядок сортировки от меньшего к большему')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:products_cat', args=(self.slug,))

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'
        ordering = ('order',)


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(avaible=True)

    def newest(self):
        return super().get_queryset().filter(avaible=True, new=True)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name='products', verbose_name='Категория товаров')
    name = models.CharField(max_length=40, verbose_name='Название товара')
    slug = models.SlugField(max_length=40, unique=True, db_index=True,
                            verbose_name='Интернет имя товара(slug)')
    description = models.TextField(blank=True,
                                   verbose_name='Описание товара')
    image = models.ImageField(upload_to=get_product_main_image_path, blank=True,
                              verbose_name='Основное изображение')
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2,
                                verbose_name='Цена')
    avaible = models.BooleanField(default=True, db_index=True,
                                  verbose_name='Товар доступен к продаже')
    new = models.BooleanField(default=False, db_index=True,
                              verbose_name='Новинка')
    added = models.DateTimeField(auto_now_add=True, db_index=True)
    image_quantity = models.PositiveSmallIntegerField(
        default=1, editable=False)

    objects = models.Manager()
    show = ProductManager()

    def __str__(self):
        return self.slug

    def delete(self, *args, **kwargs):
        for image in self.images.all():
            image.delete()
        super().delete(*args, **kwargs)

    def increment_image(self):
        self.image_quantity += 1
        self.save()

    def get_absolute_url(self):
        return reverse('store:product_detail', args=(self.slug,))

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        unique_together = ['category', 'name']
        get_latest_by = ['added']
        ordering = ['category', 'name']


class ProductExtraImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images', verbose_name='Товар')
    image = models.ImageField(upload_to=get_extra_image_path,
                              verbose_name='Изображение')

    class Meta:
        verbose_name = 'Дополнительное изображение товара'
        verbose_name_plural = 'Дополнительные изображеия товара'
