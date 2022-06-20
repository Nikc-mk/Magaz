from django.shortcuts import get_object_or_404, render

from .forms import CommentForm
from .models import Post, Comment
from django.views.generic import ListView, DetailView


# Create your views here.
class PostList(ListView):
    model = Post
    queryset = Post.objects.filter(status='published')
    template_name = 'blog/post/post_list.html'
    # context_object_name = 'latest_post_list'
    paginate_by = 3  # атрибут предоставляет встроенный способ постраничного отображения списка


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post/post_detail.html'
    context_object_name = 'post'  # Объект в шаблоне называется object. Иногда это может сбивать с толку, и вам может
    # понадобиться изменить его. Переопределите атрибут context_object_name. Отныне в шаблоне
    # вы можете использовать новое имя вашего объекта.
    extra_context = {'latest': Post.objects.all()[:3]}  # Давайте попробуем добавить три поста в контекст.


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post)
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})
