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