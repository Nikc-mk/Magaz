from django.db import models
from django.urls import reverse
from django.forms import ModelForm
from taggit.managers import TaggableManager
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    """    Статьи    """
    draft = models.BooleanField('Черновик', default=True)
    title = models.CharField('Заглавие', max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    # это поле, предназначенное для использования в URL-адресах
    # Мы добавили параметр unique_for_date в это поле, чтобы можно было построить уникальные URL-адреса содержащие
    # title поста и дату его публикации.
    image = models.ImageField('Изображения', upload_to='static/img/post', null=True)
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    # Джанго автоматически создает первичный ключ для каждой модели, но можно также переопределить это задание
    # primary_key=True в одном из полей модели.

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        # db_table = 'post'  # Джанго создает имена таблиц, сочетая имя приложения и строчное имя модели (blog_post),
        # но можно также указать их в классе Meta модели, используя атрибут db_table.

    def __str__(self):
        return self.title

    # создаем функцию для получения ссылки на пост
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField('Имя', max_length=80)
    text = models.TextField('Текст')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"{self.name} - {self.post}"


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'post', 'text']
