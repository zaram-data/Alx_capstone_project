from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.models import Post, Follow, Like
from api.serializers import PostSerializer, FollowSerializer, LikeSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

# ---------------- Post Views ----------------

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist"}, status=404)
        
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        return Response({"created": created})

class UnlikePost(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        
        if deleted:
            return Response({'detail': 'Like removed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'You had not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
	

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
