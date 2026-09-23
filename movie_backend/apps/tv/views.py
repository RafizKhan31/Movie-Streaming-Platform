from django.db.models import Q
from rest_framework import permissions
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from common.responses import APIResponse
from common.pagination import StandardResultsSetPagination
from .models import TVSeries, Season, Episode
from .serializers import (
    TVSeriesListSerializer,
    TVSeriesDetailSerializer,
    SeasonSerializer,
    EpisodeListSerializer,
    EpisodeDetailSerializer,
)


class TVSeriesListView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="List TV series with filtering and pagination",
        parameters=[
            OpenApiParameter('genre', str, description="Filter by genre slug"),
            OpenApiParameter('category', str, description="Filter by category (tv_series, web_series, anime, kids)"),
            OpenApiParameter('search', str, description="Search term"),
            OpenApiParameter('ordering', str, description="Order by: -imdb_rating, -release_date, -views"),
        ],
    )
    def get(self, request):
        queryset = TVSeries.objects.filter(is_active=True).prefetch_related('genres').distinct()

        genre_param = request.query_params.get('genre')
        if genre_param:
            queryset = queryset.filter(Q(genres__slug=genre_param) | Q(genres__name__iexact=genre_param))

        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category.lower())

        search = request.query_params.get('search') or request.query_params.get('q')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(cast__name__icontains=search)
            ).distinct()

        ordering = request.query_params.get('ordering', '-release_date')
        if ordering in ['-release_date', 'release_date', '-imdb_rating', 'imdb_rating', '-views', 'views']:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-release_date')

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = TVSeriesListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class TVSeriesDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Get TV Series details with seasons and episodes")
    def get(self, request, identifier):
        queryset = TVSeries.objects.filter(is_active=True).prefetch_related(
            'genres',
            'cast',
            'directors',
            'seasons__episodes',
        )

        series = None
        if identifier.isdigit():
            series = queryset.filter(id=int(identifier)).first()
        if not series:
            series = queryset.filter(slug=identifier).first()

        if not series:
            return APIResponse.error(message="TV Series not found.", status_code=404)

        serializer = TVSeriesDetailSerializer(series, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Series details retrieved.")


class TVSeriesSeasonsView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Get seasons for a TV series")
    def get(self, request, identifier):
        series = TVSeries.objects.filter(slug=identifier).first()
        if not series and identifier.isdigit():
            series = TVSeries.objects.filter(id=int(identifier)).first()

        if not series:
            return APIResponse.error(message="Series not found.", status_code=404)

        seasons = series.seasons.all().prefetch_related('episodes')
        serializer = SeasonSerializer(seasons, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Seasons retrieved.")


class TVSeriesEpisodesView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Get all episodes of a TV series")
    def get(self, request, identifier):
        series = TVSeries.objects.filter(slug=identifier).first()
        if not series and identifier.isdigit():
            series = TVSeries.objects.filter(id=int(identifier)).first()

        if not series:
            return APIResponse.error(message="Series not found.", status_code=404)

        episodes = Episode.objects.filter(season__series=series, is_active=True).order_by('season__season_number', 'episode_number')
        serializer = EpisodeListSerializer(episodes, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Episodes retrieved.")


class EpisodeDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Get episode details with streaming info and subtitles")
    def get(self, request, pk):
        try:
            episode = Episode.objects.select_related('season__series').prefetch_related('episode_video_sources', 'episode_subtitles').get(pk=pk, is_active=True)
        except Episode.DoesNotExist:
            return APIResponse.error(message="Episode not found.", status_code=404)

        serializer = EpisodeDetailSerializer(episode, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Episode details retrieved.")
