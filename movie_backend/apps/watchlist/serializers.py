from rest_framework import serializers
from apps.movies.serializers import MovieListSerializer
from apps.tv.serializers import TVSeriesListSerializer
from apps.movies.models import Movie
from apps.tv.models import TVSeries
from .models import Watchlist, Favorite


class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)
    series = TVSeriesListSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source='movie', write_only=True, required=False, allow_null=True
    )
    series_id = serializers.PrimaryKeyRelatedField(
        queryset=TVSeries.objects.all(), source='series', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Watchlist
        fields = ['id', 'movie', 'series', 'movie_id', 'series_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        movie = attrs.get('movie')
        series = attrs.get('series')
        if not movie and not series:
            raise serializers.ValidationError("Must provide either movie_id or series_id.")
        if movie and series:
            raise serializers.ValidationError("Cannot provide both movie_id and series_id simultaneously.")
        return attrs


class FavoriteSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)
    series = TVSeriesListSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source='movie', write_only=True, required=False, allow_null=True
    )
    series_id = serializers.PrimaryKeyRelatedField(
        queryset=TVSeries.objects.all(), source='series', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Favorite
        fields = ['id', 'movie', 'series', 'movie_id', 'series_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        movie = attrs.get('movie')
        series = attrs.get('series')
        if not movie and not series:
            raise serializers.ValidationError("Must provide either movie_id or series_id.")
        if movie and series:
            raise serializers.ValidationError("Cannot provide both movie_id and series_id simultaneously.")
        return attrs
