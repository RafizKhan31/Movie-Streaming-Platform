from rest_framework import serializers
from .models import Genre


class GenreSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug', 'description', 'icon', 'movies_count', 'created_at']
