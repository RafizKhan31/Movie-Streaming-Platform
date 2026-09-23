from rest_framework import serializers
from apps.accounts.serializers import UserSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'movie',
            'series',
            'rating',
            'title',
            'content',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'movie', 'series', 'created_at', 'updated_at']
