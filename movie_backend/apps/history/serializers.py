from rest_framework import serializers
from apps.movies.serializers import MovieListSerializer
from apps.tv.serializers import EpisodeListSerializer
from apps.movies.models import Movie
from apps.tv.models import Episode
from .models import WatchHistory


class WatchHistorySerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)
    episode = EpisodeListSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source='movie', write_only=True, required=False, allow_null=True
    )
    episode_id = serializers.PrimaryKeyRelatedField(
        queryset=Episode.objects.all(), source='episode', write_only=True, required=False, allow_null=True
    )
    progress_percentage = serializers.FloatField(read_only=True)
    progress_display = serializers.CharField(read_only=True)

    class Meta:
        model = WatchHistory
        fields = [
            'id',
            'movie',
            'episode',
            'movie_id',
            'episode_id',
            'current_position',
            'duration',
            'progress_percentage',
            'progress_display',
            'completed',
            'last_watched',
        ]
        read_only_fields = ['id', 'progress_percentage', 'progress_display', 'last_watched']

    def validate(self, attrs):
        movie = attrs.get('movie')
        episode = attrs.get('episode')
        if not movie and not episode:
            raise serializers.ValidationError("Must provide either movie_id or episode_id.")
        if movie and episode:
            raise serializers.ValidationError("Cannot provide both movie_id and episode_id.")
        return attrs
