from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.models import Post, Follow, Like
from api.serializers import PostSerializer, FollowSerializer, LikeSerializer
from django.contrib.auth.models import User

# ---------------- Post Views ----------------

class PostList(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PostCreate(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# ---------------- Feed ----------------

class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# ---------------- Follow / Unfollow ----------------

class FollowUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response({'detail': 'cannot follow yourself'}, status=400)
        obj, created = Follow.objects.get_or_create(follower=request.user, following_id=user_id)
        return Response({'created': created})

class UnfollowUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        Follow.objects.filter(follower=request.user, following_id=user_id).delete()
        return Response({'deleted': True})

# ---------------- Like / Unlike ----------------

class LikePost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        obj, created = Like.objects.get_or_create(user=request.user, post_id=post_id)
        return Response({'created': created})

class UnlikePost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        Like.objects.filter(user=request.user, post_id=post_id).delete()
        return Response({'deleted': True})

# ---------------- API Root ----------------

class ApiRoot(APIView):
    permission_classes = [permissions.AllowAny]  # optional, public
    def get(self, request):
        return Response({
            "posts": "/api/posts/",
            "create_post": "/api/posts/create/",
            "feed": "/api/feed/",
            "follow": "/api/follow/<user_id>/",
            "unfollow": "/api/unfollow/<user_id>/",
            "like": "/api/like/<post_id>/",
            "unlike": "/api/unlike/<post_id>/",
        })
