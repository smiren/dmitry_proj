from django.db import models
from django.urls import reverse
from .utils import get_infopage_image_path

class InfoPages(models.Model):
    title = models.CharField(max_length=50,
        verbose_name='Заглавие страницы (title)')
    slug = models.SlugField(max_length=12, db_index=True, unique=True,
        verbose_name='интернет имя страницы (slug)')
    menuname = models.CharField(max_length=30,
        verbose_name='Имя страницы в нав-меню')
    headline = models.CharField(max_length=100,
        verbose_name='Заголовок страницы (h1)')
    head_text = models.TextField(blank=True,
        verbose_name='Текст под заголовком страницы')
    content_text = models.TextField(blank=True,
        verbose_name='Основной текст страницы',
        help_text='Данное поле заполняется в HTML разметке')
    image_quantity = models.PositiveSmallIntegerField(default=0, editable=False)

    def get_absolute_url(self):
        return reverse('main:infopage', args=[self.slug])

    def __str__(self):
        return self.menuname

    def increment_image(self):
        self.image_quantity += 1
        self.save()

    class Meta:
        verbose_name = "Информационная сраница"
        verbose_name_plural = "Страницы информации"

def get_upload_image_path(instance, filename):
    imagefile = "{0:0>8}.{1}".format(instance.pagename.image_quantity ,filename.split('.')[1])
    path = 'infopages/' + instance.pagename.slug +'/'+ imagefile
    instance.pagename.increment_image()
    return path

class InfoPageImages(models.Model):
    pagename = models.ForeignKey(InfoPages, on_delete=models.CASCADE ,
        related_name="images", verbose_name='Инфо-страница')
    image = models.ImageField(upload_to=get_infopage_image_path,
        verbose_name='Изображение')
    imagename = models.CharField(max_length=100, blank=True,
        verbose_name='Название изображения')
    imagedesc = models.TextField(blank=True,
        verbose_name='Описание изображения')

    class Meta:
        verbose_name = "Изображение для инфо-страницы"
        verbose_name_plural = "Изображения для инфо-страниц"
