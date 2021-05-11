from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/create', views.PostCreateView.as_view(), name='post-create'),
    path('posts/delete/<int:pk>', views.PostDeleteView.as_view(), name='post-delete'),
    path('posts/my', views.MyPostListView.as_view(), name='my-post-list'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('comments/add/<int:pk>', views.CommentPostView.as_view(), name='comment-post'),
    path('comments/delete/<int:pk>', views.CommentDeleteView.as_view(), name='comment-delete'),
]
