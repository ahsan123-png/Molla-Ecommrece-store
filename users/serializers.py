from rest_framework import serializers
from . import models
# from .stripe import serializers as stripe_serializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserEx
        fields = (
            'id',
            'username',
            'email',
            'phone',
            "name",
            "gender",
            "date_of_birth",
            "date_joined"

        )