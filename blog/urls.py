from django.urls import re_path, path
from . import views

urlpatterns = [
    # post views
    path('blog/', views.PostList.as_view(), name='post_list'),
    path('blog/<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
]
