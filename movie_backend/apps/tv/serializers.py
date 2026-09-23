from rest_framework import serializers
from apps.genres.serializers import GenreSerializer
from apps.movies.serializers import PersonSerializer
from .models import TVSeries, Season, Episode


class EpisodeListSerializer(serializers.ModelSerializer):
    thumbnail_display = serializers.CharField(source='get_thumbnail_display', read_only=True)

    class Meta:
        model = Episode
        fields = [
            'id',
            'episode_number',
            'title',
            'description',
            'thumbnail_display',
            'duration',
            'duration_minutes',
            'release_date',
            'trailer_url',
            'views',
        ]


class EpisodeDetailSerializer(serializers.ModelSerializer):
    thumbnail_display = serializers.CharField(source='get_thumbnail_display', read_only=True)
    video_sources = serializers.SerializerMethodField()
    subtitles = serializers.SerializerMethodField()
    series_title = serializers.CharField(source='season.series.title', read_only=True)
    season_number = serializers.IntegerField(source='season.season_number', read_only=True)

    class Meta:
        model = Episode
        fields = [
            'id',
            'series_title',
            'season_number',
            'episode_number',
            'title',
            'description',
            'thumbnail_display',
            'duration',
            'duration_minutes',
            'release_date',
            'video_url',
            'trailer_url',
            'views',
            'video_sources',
            'subtitles',
        ]

    def get_video_sources(self, obj):
        from apps.streaming.serializers import VideoSourceSerializer
        sources = obj.episode_video_sources.filter(is_active=True).order_by('quality')
        return VideoSourceSerializer(sources, many=True, context=self.context).data

    def get_subtitles(self, obj):
        from apps.streaming.serializers import SubtitleSerializer
        subs = obj.episode_subtitles.all().order_by('language')
        return SubtitleSerializer(subs, many=True, context=self.context).data


class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeListSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = ['id', 'season_number', 'title', 'description', 'poster', 'release_date', 'episodes']


class TVSeriesListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    poster_display = serializers.CharField(source='get_poster_display', read_only=True)
    backdrop_display = serializers.CharField(source='get_backdrop_display', read_only=True)

    class Meta:
        model = TVSeries
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'poster_display',
            'backdrop_display',
            'trailer_url',
            'release_year',
            'imdb_rating',
            'genres',
            'category',
            'featured',
            'trending',
            'views',
        ]


class TVSeriesDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    cast = PersonSerializer(many=True, read_only=True)
    directors = PersonSerializer(many=True, read_only=True)
    seasons = SeasonSerializer(many=True, read_only=True)
    poster_display = serializers.CharField(source='get_poster_display', read_only=True)
    backdrop_display = serializers.CharField(source='get_backdrop_display', read_only=True)
    in_watchlist = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = TVSeries
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'poster_display',
            'backdrop_display',
            'trailer_url',
            'release_date',
            'release_year',
            'age_rating',
            'imdb_rating',
            'tmdb_rating',
            'views',
            'featured',
            'trending',
            'category',
            'genres',
            'cast',
            'directors',
            'seasons',
            'in_watchlist',
            'is_favorite',
            'created_at',
            'updated_at',
        ]

    def get_in_watchlist(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.watchlist_items.filter(user=request.user).exists()
        return False

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorite_items.filter(user=request.user).exists()
        return False
