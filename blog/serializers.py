from rest_framework import serializers
from . import models
# from .stripe import serializers as stripe_serializer

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BlogPost
        fields = (
            'id',
            'title',
            'subject',
            'description',
            "publish_date",
            "user",
            "picture",
            "like_count"

        )
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = (
            'user',
            'blog_post',
            'created_at',
        )
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = (
            'user',
            'blog_post',
            'text',
            'parent_comment',
            "created_at",
 
        )