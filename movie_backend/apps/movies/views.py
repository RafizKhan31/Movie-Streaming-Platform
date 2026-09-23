from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_spectacular.utils import extend_schema, OpenApiParameter

from common.responses import APIResponse
from common.pagination import StandardResultsSetPagination
from .models import Movie, MovieSubmission
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    MovieSubmissionSerializer,
)


class MovieListView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="List movies with filtering, sorting, searching, and pagination",
        parameters=[
            OpenApiParameter('genre', str, description="Filter by genre slug or id"),
            OpenApiParameter('category', str, description="Filter by category (hollywood, bollywood, kids, etc.)"),
            OpenApiParameter('year', int, description="Filter by release year"),
            OpenApiParameter('min_rating', float, description="Filter by minimum IMDb rating"),
            OpenApiParameter('search', str, description="Search by title, description, cast, director"),
            OpenApiParameter('ordering', str, description="Ordering: -release_date, -imdb_rating, -views, etc."),
        ],
    )
    def get(self, request):
        queryset = Movie.objects.filter(is_active=True).prefetch_related('genres').distinct()

        # Filtering
        genre_param = request.query_params.get('genre')
        if genre_param:
            queryset = queryset.filter(Q(genres__slug=genre_param) | Q(genres__name__iexact=genre_param))

        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category.lower())

        year = request.query_params.get('year')
        if year:
            try:
                queryset = queryset.filter(release_year=int(year))
            except ValueError:
                pass

        min_rating = request.query_params.get('min_rating')
        if min_rating:
            try:
                queryset = queryset.filter(imdb_rating__gte=float(min_rating))
            except ValueError:
                pass

        featured = request.query_params.get('featured')
        if featured is not None:
            queryset = queryset.filter(featured=featured.lower() in ('true', '1'))

        trending = request.query_params.get('trending')
        if trending is not None:
            queryset = queryset.filter(trending=trending.lower() in ('true', '1'))

        # Search
        search = request.query_params.get('search') or request.query_params.get('q')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(tags__icontains=search) |
                Q(cast__name__icontains=search) |
                Q(directors__name__icontains=search)
            ).distinct()

        # Ordering
        ordering = request.query_params.get('ordering', '-release_date')
        allowed_orderings = ['release_date', '-release_date', 'imdb_rating', '-imdb_rating', 'views', '-views', 'title', '-title']
        if ordering in allowed_orderings:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-release_date')

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = MovieListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class MovieDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Get full movie details by ID or Slug")
    def get(self, request, identifier):
        queryset = Movie.objects.filter(is_active=True).prefetch_related(
            'genres',
            'movie_cast__person',
            'directors',
            'writers',
            'video_sources',
            'subtitles',
        )

        movie = None
        if identifier.isdigit():
            movie = queryset.filter(id=int(identifier)).first()
        if not movie:
            movie = queryset.filter(slug=identifier).first()

        if not movie:
            return APIResponse.error(message="Movie not found.", status_code=404)

        serializer = MovieDetailSerializer(movie, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Movie details retrieved.")


class MovieTrendingView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Get top trending movies")
    def get(self, request):
        movies = Movie.objects.filter(is_active=True, trending=True).prefetch_related('genres').order_by('-views')[:15]
        serializer = MovieListSerializer(movies, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Trending movies retrieved.")


class MoviePopularView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Get most popular movies by views/rating")
    def get(self, request):
        movies = Movie.objects.filter(is_active=True).prefetch_related('genres').order_by('-views', '-imdb_rating')[:15]
        serializer = MovieListSerializer(movies, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Popular movies retrieved.")


class MovieLatestView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Get recently released movies")
    def get(self, request):
        movies = Movie.objects.filter(is_active=True).prefetch_related('genres').order_by('-release_date', '-id')[:15]
        serializer = MovieListSerializer(movies, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Latest movies retrieved.")


class MovieFeaturedView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Get featured movies for hero slider")
    def get(self, request):
        movies = Movie.objects.filter(is_active=True, featured=True).prefetch_related('genres').order_by('-views')[:10]
        serializer = MovieListSerializer(movies, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Featured movies retrieved.")


class MovieTopRatedView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Get top rated movies")
    def get(self, request):
        movies = Movie.objects.filter(is_active=True).prefetch_related('genres').order_by('-imdb_rating')[:15]
        serializer = MovieListSerializer(movies, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Top rated movies retrieved.")


class MovieSubmitView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @extend_schema(
        request=MovieSubmissionSerializer,
        summary="Submit movie suggestion with poster upload",
    )
    def post(self, request):
        serializer = MovieSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            submission = serializer.save()
            return APIResponse.success(
                data=serializer.data,
                message="Movie submitted successfully. Our team will review it shortly.",
                status_code=status.HTTP_201_CREATED,
            )
        return APIResponse.error(
            message="Submission failed. Please check the provided information.",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
