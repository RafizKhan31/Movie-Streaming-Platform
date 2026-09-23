from rest_framework import permissions, status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from common.responses import APIResponse
from .models import Watchlist, Favorite
from .serializers import WatchlistSerializer, FavoriteSerializer


class WatchlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Get current user's watchlist")
    def get(self, request):
        items = Watchlist.objects.filter(user=request.user).select_related('movie', 'series')
        serializer = WatchlistSerializer(items, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Watchlist retrieved successfully.")

    @extend_schema(request=WatchlistSerializer, summary="Add movie or series to watchlist")
    def post(self, request):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            movie = serializer.validated_data.get('movie')
            series = serializer.validated_data.get('series')

            # Check if already in watchlist
            existing = Watchlist.objects.filter(user=request.user, movie=movie, series=series).first()
            if existing:
                return APIResponse.success(
                    data=WatchlistSerializer(existing, context={'request': request}).data,
                    message="Item is already in your watchlist.",
                )

            item = serializer.save(user=request.user)
            return APIResponse.success(
                data=WatchlistSerializer(item, context={'request': request}).data,
                message="Added to watchlist.",
                status_code=status.HTTP_201_CREATED,
            )
        return APIResponse.error(message="Invalid data.", errors=serializer.errors)


class WatchlistDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Remove item from watchlist by item ID or query params")
    def delete(self, request, pk=None):
        if pk:
            item = Watchlist.objects.filter(user=request.user, pk=pk).first()
        else:
            movie_id = request.query_params.get('movie_id')
            series_id = request.query_params.get('series_id')
            item = Watchlist.objects.filter(user=request.user, movie_id=movie_id, series_id=series_id).first()

        if not item:
            return APIResponse.error(message="Watchlist item not found.", status_code=404)

        item.delete()
        return APIResponse.success(message="Item removed from watchlist.")


class FavoritesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Get current user's favorites")
    def get(self, request):
        items = Favorite.objects.filter(user=request.user).select_related('movie', 'series')
        serializer = FavoriteSerializer(items, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Favorites retrieved successfully.")

    @extend_schema(request=FavoriteSerializer, summary="Add movie or series to favorites")
    def post(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            movie = serializer.validated_data.get('movie')
            series = serializer.validated_data.get('series')

            existing = Favorite.objects.filter(user=request.user, movie=movie, series=series).first()
            if existing:
                return APIResponse.success(
                    data=FavoriteSerializer(existing, context={'request': request}).data,
                    message="Item is already in your favorites.",
                )

            item = serializer.save(user=request.user)
            return APIResponse.success(
                data=FavoriteSerializer(item, context={'request': request}).data,
                message="Added to favorites.",
                status_code=status.HTTP_201_CREATED,
            )
        return APIResponse.error(message="Invalid data.", errors=serializer.errors)


class FavoriteDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Remove item from favorites by item ID or query params")
    def delete(self, request, pk=None):
        if pk:
            item = Favorite.objects.filter(user=request.user, pk=pk).first()
        else:
            movie_id = request.query_params.get('movie_id')
            series_id = request.query_params.get('series_id')
            item = Favorite.objects.filter(user=request.user, movie_id=movie_id, series_id=series_id).first()

        if not item:
            return APIResponse.error(message="Favorite item not found.", status_code=404)

        item.delete()
        return APIResponse.success(message="Item removed from favorites.")
