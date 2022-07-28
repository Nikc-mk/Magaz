from .models import Post, Comment
from django.views.generic import ListView, DetailView
from taggit.models import Tag


# Create your views here.
class PostList(ListView):
    model = Post
    queryset = Post.objects.filter(draft=False)
    template_name = 'blog/post/post_list.html'
    # context_object_name = 'latest_post_list'
    paginate_by = 4  # атрибут предоставляет встроенный способ постраничного отображения списка


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post/post_detail.html'
    context_object_name = 'post'  # Объект в шаблоне называется object. Иногда это может сбивать с толку, и вам может
    # понадобиться изменить его. Переопределите атрибут context_object_name. Отныне в шаблоне
    # вы можете использовать новое имя вашего объекта.
    slug_field = "slug"
    extra_context = {'latest': Post.objects.all()[:3]}  # Давайте попробуем добавить три поста в контекст.


class CommentList(ListView):
    model = Comment
    template_name = 'blog/post/post_detail.html'
    context_object_name = 'comment_list'
