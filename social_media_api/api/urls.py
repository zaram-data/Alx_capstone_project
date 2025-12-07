from .views import ApiRoot
from django.urls import path
from api import views

urlpatterns = [
    path('', ApiRoot.as_view(), name='api-root'),  # 👈 Add this
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/create/', views.PostCreate.as_view(), name='post-create'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('follow/<int:user_id>/', views.FollowUser.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', views.UnfollowUser.as_view(), name='unfollow'),
    path('like/<int:post_id>/', views.LikePost.as_view(), name='like'),
    path('unlike/<int:post_id>/', views.UnlikePost.as_view(), name='unlike'),
]
