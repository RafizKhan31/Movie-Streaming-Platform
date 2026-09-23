from rest_framework import serializers
from apps.genres.serializers import GenreSerializer
from .models import Person, Movie, MovieCast, MovieSubmission


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'role', 'bio', 'photo']


class MovieCastSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    person_id = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(), source='person', write_only=True
    )

    class Meta:
        model = MovieCast
        fields = ['id', 'person', 'person_id', 'character_name', 'order']


class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    poster_display = serializers.CharField(source='get_poster_display', read_only=True)
    backdrop_display = serializers.CharField(source='get_backdrop_display', read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'poster',
            'poster_display',
            'backdrop_display',
            'trailer_url',
            'release_year',
            'duration',
            'imdb_rating',
            'genres',
            'category',
            'featured',
            'trending',
            'views',
        ]


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    movie_cast = MovieCastSerializer(many=True, read_only=True)
    directors = PersonSerializer(many=True, read_only=True)
    writers = PersonSerializer(many=True, read_only=True)
    poster_display = serializers.CharField(source='get_poster_display', read_only=True)
    backdrop_display = serializers.CharField(source='get_backdrop_display', read_only=True)
    video_sources = serializers.SerializerMethodField()
    subtitles = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    in_watchlist = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'poster',
            'poster_display',
            'backdrop',
            'backdrop_display',
            'thumbnail',
            'trailer_url',
            'release_date',
            'release_year',
            'duration',
            'duration_minutes',
            'language',
            'country',
            'age_rating',
            'content_rating',
            'status',
            'imdb_rating',
            'tmdb_rating',
            'views',
            'featured',
            'trending',
            'category',
            'genres',
            'movie_cast',
            'directors',
            'writers',
            'tags',
            'video_sources',
            'subtitles',
            'user_rating',
            'in_watchlist',
            'is_favorite',
            'created_at',
            'updated_at',
        ]

    def get_video_sources(self, obj):
        from apps.streaming.serializers import VideoSourceSerializer
        sources = obj.video_sources.filter(is_active=True).order_by('quality')
        return VideoSourceSerializer(sources, many=True, context=self.context).data

    def get_subtitles(self, obj):
        from apps.streaming.serializers import SubtitleSerializer
        subs = obj.subtitles.all().order_by('language')
        return SubtitleSerializer(subs, many=True, context=self.context).data

    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            review = obj.reviews.filter(user=request.user).first()
            if review:
                return review.rating
        return None

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


class MovieSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSubmission
        fields = ['id', 'movie_name', 'release_year', 'genre', 'description', 'poster', 'email', 'agree_terms', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']
