
from rest_framework import serializers
from api.models import Follow

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id','follower','following','created_at']
        read_only_fields = ['created_at']
