from django.core.cache import cache
from rest_framework import permissions, status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from common.responses import APIResponse
from apps.movies.models import Movie
from apps.tv.models import TVSeries
from apps.genres.models import Genre
from apps.history.models import WatchHistory
from apps.movies.serializers import MovieListSerializer
from apps.tv.serializers import TVSeriesListSerializer
from apps.genres.serializers import GenreSerializer
from apps.history.serializers import WatchHistorySerializer
from .models import ContactMessage
from .serializers import ContactMessageSerializer


class HomePageView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Optimized single-endpoint API for homepage data",
        description="Returns featured, trending, popular, latest movies, latest series, top rated, genres, and personalized continue watching data."
    )
    def get(self, request):
        cache_key = "homepage_public_data"
        public_data = cache.get(cache_key)

        if not public_data:
            featured = Movie.objects.filter(is_active=True, featured=True).prefetch_related('genres')[:8]
            trending = Movie.objects.filter(is_active=True, trending=True).prefetch_related('genres')[:10]
            popular = Movie.objects.filter(is_active=True).prefetch_related('genres').order_by('-views', '-imdb_rating')[:10]
            latest_movies = Movie.objects.filter(is_active=True).prefetch_related('genres').order_by('-release_date')[:10]
            latest_series = TVSeries.objects.filter(is_active=True).prefetch_related('genres').order_by('-release_date')[:10]
            top_rated = Movie.objects.filter(is_active=True).prefetch_related('genres').order_by('-imdb_rating')[:10]
            genres = Genre.objects.all().order_by('name')

            public_data = {
                "featured": MovieListSerializer(featured, many=True, context={'request': request}).data,
                "trending": MovieListSerializer(trending, many=True, context={'request': request}).data,
                "popular": MovieListSerializer(popular, many=True, context={'request': request}).data,
                "latest_movies": MovieListSerializer(latest_movies, many=True, context={'request': request}).data,
                "latest_series": TVSeriesListSerializer(latest_series, many=True, context={'request': request}).data,
                "top_rated": MovieListSerializer(top_rated, many=True, context={'request': request}).data,
                "genres": GenreSerializer(genres, many=True).data,
            }
            # Cache for 5 minutes
            cache.set(cache_key, public_data, 300)

        # Append personalized continue watching if user is authenticated
        continue_watching = []
        if request.user.is_authenticated:
            history = WatchHistory.objects.filter(user=request.user, completed=False).select_related(
                'movie', 'episode__season__series'
            ).order_by('-last_watched')[:6]
            continue_watching = WatchHistorySerializer(history, many=True, context={'request': request}).data

        response_data = dict(public_data)
        response_data["continue_watching"] = continue_watching

        return APIResponse.success(data=response_data, message="Homepage data retrieved successfully.")


class ContactView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=ContactMessageSerializer, summary="Submit a contact inquiry")
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.success(
                data=serializer.data,
                message="Thank you! Your message has been sent successfully. We will get back to you soon.",
                status_code=status.HTTP_201_CREATED,
            )
        return APIResponse.error(message="Please fill in all required fields properly.", errors=serializer.errors)
