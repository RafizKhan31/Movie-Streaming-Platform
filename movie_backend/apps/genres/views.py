from django.db.models import Count
from rest_framework import generics, permissions
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from common.responses import APIResponse
from .models import Genre
from .serializers import GenreSerializer


class GenreListView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="List all genres with movie counts")
    def get(self, request):
        genres = Genre.objects.annotate(movies_count=Count('movies')).order_by('name')
        serializer = GenreSerializer(genres, many=True)
        return APIResponse.success(data=serializer.data, message="Genres retrieved successfully.")


class GenreDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Get genre details by slug")
    def get(self, request, slug):
        try:
            genre = Genre.objects.annotate(movies_count=Count('movies')).get(slug=slug)
        except Genre.DoesNotExist:
            return APIResponse.error(message="Genre not found.", errors={"slug": "Not found"}, status_code=404)
        serializer = GenreSerializer(genre)
        return APIResponse.success(data=serializer.data, message="Genre details retrieved.")


class GenreMoviesView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="List all movies for a given genre")
    def get(self, request, slug):
        from apps.movies.models import Movie
        from apps.movies.serializers import MovieListSerializer
        from common.pagination import StandardResultsSetPagination

        try:
            genre = Genre.objects.get(slug=slug)
        except Genre.DoesNotExist:
            return APIResponse.error(message="Genre not found.", status_code=404)

        movies = Movie.objects.filter(genres=genre, is_active=True).select_related().prefetch_related('genres').order_by('-release_date')
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(movies, request)
        serializer = MovieListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
