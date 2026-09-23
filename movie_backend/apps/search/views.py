from django.db.models import Q
from rest_framework import permissions
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from common.responses import APIResponse
from apps.movies.models import Movie, Person
from apps.tv.models import TVSeries
from apps.genres.models import Genre
from apps.movies.serializers import MovieListSerializer, PersonSerializer
from apps.tv.serializers import TVSeriesListSerializer
from apps.genres.serializers import GenreSerializer


class UnifiedSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Unified search across movies, tv series, people, and genres",
        parameters=[
            OpenApiParameter('q', str, required=True, description="Search query string"),
            OpenApiParameter('type', str, description="Filter result type: all, movie, series, person"),
            OpenApiParameter('limit', int, description="Max results per category (default: 10)"),
        ]
    )
    def get(self, request):
        query = (request.query_params.get('q') or request.query_params.get('search') or '').strip()
        if not query:
            return APIResponse.success(
                data={"movies": [], "series": [], "people": [], "genres": [], "total_results": 0},
                message="No search query provided."
            )

        search_type = request.query_params.get('type', 'all').lower()
        limit = int(request.query_params.get('limit', 12))

        movies_data = []
        series_data = []
        people_data = []
        genres_data = []

        if search_type in ('all', 'movie', 'movies'):
            movies = Movie.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__icontains=query) |
                Q(cast__name__icontains=query) |
                Q(directors__name__icontains=query),
                is_active=True
            ).distinct().prefetch_related('genres')[:limit]
            movies_data = MovieListSerializer(movies, many=True, context={'request': request}).data

        if search_type in ('all', 'series', 'tv'):
            series = TVSeries.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(cast__name__icontains=query),
                is_active=True
            ).distinct().prefetch_related('genres')[:limit]
            series_data = TVSeriesListSerializer(series, many=True, context={'request': request}).data

        if search_type in ('all', 'person', 'people'):
            people = Person.objects.filter(
                Q(name__icontains=query) | Q(bio__icontains=query)
            )[:limit]
            people_data = PersonSerializer(people, many=True, context={'request': request}).data

        if search_type in ('all', 'genre', 'genres'):
            genres = Genre.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )[:limit]
            genres_data = GenreSerializer(genres, many=True).data

        total = len(movies_data) + len(series_data) + len(people_data) + len(genres_data)

        return APIResponse.success(
            data={
                "query": query,
                "total_results": total,
                "movies": movies_data,
                "series": series_data,
                "people": people_data,
                "genres": genres_data,
            },
            message=f"Found {total} results for '{query}'."
        )
