from rest_framework import generics, permissions
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from .serializers import UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Follow




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = User.objects.get(id=user_id)
        Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        return Response({"message": "User followed"})


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)

        follow_instance = Follow.objects.filter(
            follower=request.user,
            following=user_to_unfollow
        ).first()

        if not follow_instance:
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        follow_instance.delete()

        return Response(
            {"detail": "User unfollowed successfully."},
            status=status.HTTP_200_OK
        )