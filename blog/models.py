from django.db import models
from django.urls import reverse

from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    status_choices = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)  # название
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # это поле, предназначенное для использования в URL-адресах
    # Мы добавили параметр unique_for_date в это поле, чтобы можно было построить уникальные URL-адреса содержащие
    # title поста и дату его публикации.
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=status_choices, default='draft')

    # Джанго автоматически создает первичный ключ для каждой модели, но можно также переопределить это задание
    # primary_key=True в одном из полей модели.

    class Meta:
        ordering = ('-publish',)
        db_table = 'post'  # Джанго создает имена таблиц, сочетая имя приложения и строчное имя модели (blogpost),
        # но можно также указать их в классе Meta модели, используя атрибут db_table.

    def __str__(self):
        return self.title

    # создаем функцию для получения ссылки на пост
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
