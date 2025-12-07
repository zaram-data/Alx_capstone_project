
from rest_framework import serializers
from api.models import Post

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Post
        fields = ['id','author','author_username','content','image_url','created_at']
        read_only_fields = ['author','created_at']
