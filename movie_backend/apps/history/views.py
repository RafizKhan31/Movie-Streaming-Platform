from rest_framework import permissions, status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from common.responses import APIResponse
from .models import WatchHistory
from .serializers import WatchHistorySerializer


class WatchHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Get user's watch history (Continue Watching)",
        parameters=[
            OpenApiParameter('completed', bool, description="Filter by completed status"),
            OpenApiParameter('limit', int, description="Limit number of items"),
        ]
    )
    def get(self, request):
        history = WatchHistory.objects.filter(user=request.user).select_related('movie', 'episode__season__series')
        completed = request.query_params.get('completed')
        if completed is not None:
            history = history.filter(completed=completed.lower() in ('true', '1'))

        limit = request.query_params.get('limit')
        if limit:
            try:
                history = history[:int(limit)]
            except ValueError:
                pass

        serializer = WatchHistorySerializer(history, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Watch history retrieved successfully.")

    @extend_schema(request=WatchHistorySerializer, summary="Update playback position / save progress")
    def post(self, request):
        serializer = WatchHistorySerializer(data=request.data)
        if serializer.is_valid():
            movie = serializer.validated_data.get('movie')
            episode = serializer.validated_data.get('episode')
            current_pos = serializer.validated_data.get('current_position', 0.0)
            duration = serializer.validated_data.get('duration', 1.0)

            history, created = WatchHistory.objects.update_or_create(
                user=request.user,
                movie=movie,
                episode=episode,
                defaults={
                    'current_position': current_pos,
                    'duration': duration,
                }
            )

            result_serializer = WatchHistorySerializer(history, context={'request': request})
            return APIResponse.success(
                data=result_serializer.data,
                message="Watch progress saved.",
                status_code=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )
        return APIResponse.error(message="Invalid data.", errors=serializer.errors)


class WatchHistoryDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Update progress for a specific history record")
    def patch(self, request, pk):
        history = WatchHistory.objects.filter(pk=pk, user=request.user).first()
        if not history:
            return APIResponse.error(message="Watch history record not found.", status_code=404)

        current_position = request.data.get('current_position')
        duration = request.data.get('duration')
        if current_position is not None:
            history.current_position = float(current_position)
        if duration is not None:
            history.duration = float(duration)

        history.save()
        serializer = WatchHistorySerializer(history, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Watch history updated.")

    @extend_schema(summary="Delete a history record")
    def delete(self, request, pk):
        history = WatchHistory.objects.filter(pk=pk, user=request.user).first()
        if not history:
            return APIResponse.error(message="Record not found.", status_code=404)
        history.delete()
        return APIResponse.success(message="Record removed from watch history.")
