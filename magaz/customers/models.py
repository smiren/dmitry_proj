from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.urls import reverse
from store.models import Product
from main.utils import get_random_string
from magaz import settings

class ExtUser(AbstractUser):
    is_activeted = models.BooleanField(default=True, db_index=True,
        verbose_name='Подтвержден email?',
        help_text='Отметьте, если пользователь активирован по e-mail.')
    phone = models.CharField(max_length=10, blank=True,
        validators=[validators.RegexValidator(regex='^(|[\d]{10})$')],
        verbose_name='Номер телефона',
        help_text="Введите 10 цифр телефонного номера без восьмерки, \
        например 9031234567.")
    address = models.CharField(max_length=200, blank=True,
        verbose_name='Адрес доставки',
        help_text='Предпочтительный адрес доставки заказов.')

class BaseOrder(models.Model):
    STATUSES = (
        ('OP', 'Открыт'),
        ('CF', 'Подтвержден'),
        ('RD', 'Выполнен'),
        ('PR', 'Проблема')
    )

    phone = models.CharField(max_length=10, db_index=True,
        validators=[validators.RegexValidator(regex='^[\d]{10}$')],
        verbose_name='Номер телефона',
        help_text="Введите 10 цифр телефонного номера без восьмерки, \
        например 9031234567.")
    address = models.CharField(max_length=200, blank=True,
        verbose_name='Адрес доставки',
        help_text='Введите адрес доставки заказа.')
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')
    status = models.CharField(max_length=2, choices=STATUSES, default='OP',
        db_index=True, verbose_name='Статус заказа')
    finished = models.BooleanField(default=False, db_index=True,
        verbose_name='Завершенный заказ')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    products = models.ManyToManyField(Product, through='OrderPosition')
    total_cost = models.DecimalField(max_digits=12, decimal_places=2,
        default=0, db_index=True)
    slug = models.SlugField(max_length=20, default=get_random_string,
        db_index=True)

    def get_total_cost(self):
        total_cost = self.positions.aggregate(Sum('cost')).get('cost__sum')
        return total_cost if total_cost else 0

    def is_simple(self):
        return hasattr(self, 'simpleorder')

    def save(self, *args, set_total_cost=False, **kwargs):
        if set_total_cost:
            self.total_cost = self.get_total_cost()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('customers:order', args=[self.slug])

    def __str__(self):
        return f"Заказ № {self.id:0>8}"

    class Meta:
        verbose_name = 'Заказ(общий)'
        verbose_name_plural = 'Все заказы'
        ordering =  ['-created']

class SimpleOrder(BaseOrder):
    name = models.CharField(max_length=40, blank=True,
    verbose_name='Ваше имя')
    email = models.EmailField(null=True, db_index=True,
    verbose_name='Адрес эл.почты',
    help_text='На этот адрес будет выслана информация о заказе.')

    class Meta:
        verbose_name = 'Заказ без регистрации'
        verbose_name_plural = 'Заказы без регистрации'
        ordering =  ['-created']

class UserOrder(BaseOrder):
    user = models.ForeignKey(ExtUser, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Клиентский заказ'
        verbose_name_plural = 'Клиентские заказы'
        ordering =  ['-created']

class OrderPosition(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
        verbose_name = "Продукт")
    order = models.ForeignKey(BaseOrder, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1,
        verbose_name = "Количество")
    cost = models.DecimalField(max_digits=10, decimal_places=2,
        default=0, db_index=True, verbose_name = "Цена")

    def __str__(self):
        return f"Позиция {self.product.name}"

    class Meta:
        default_related_name = 'positions'
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

class StaffComment(models.Model):
    person = models.ForeignKey(ExtUser, on_delete=models.PROTECT,
        editable=False, default=settings.DEFAULT_USER_ID)
    order = models.ForeignKey(BaseOrder, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f"Комментарий к {self.order}"

    class Meta:
        ordering = ['-created']
        default_related_name = 'staffcomments'
        verbose_name = "Комментарий персонала"
        verbose_name_plural = "Комментарии персонала"
