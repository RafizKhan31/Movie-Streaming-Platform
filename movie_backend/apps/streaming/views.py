import os
import re
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.db.models import F
from rest_framework.views import APIView
from rest_framework import permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter

from common.responses import APIResponse
from apps.movies.models import Movie
from apps.tv.models import Episode
from .models import VideoSource, Subtitle
from .serializers import SubtitleSerializer, VideoSourceSerializer


def range_streaming_response(request, file_path, content_type='video/mp4'):
    """Helper to serve partial content range requests for video playback."""
    file_size = os.path.getsize(file_path)
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)

    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else file_size - 1
        if last_byte >= file_size:
            last_byte = file_size - 1
        length = last_byte - first_byte + 1

        def file_iterator(path, offset, length, chunk_size=8192):
            with open(path, 'rb') as f:
                f.seek(offset)
                remaining = length
                while remaining > 0:
                    read_size = min(chunk_size, remaining)
                    data = f.read(read_size)
                    if not data:
                        break
                    remaining -= len(data)
                    yield data

        response = StreamingHttpResponse(
            file_iterator(file_path, first_byte, length),
            status=206,
            content_type=content_type,
        )
        response['Content-Range'] = f'bytes {first_byte}-{last_byte}/{file_size}'
        response['Content-Length'] = str(length)
    else:
        def full_file_iterator(path, chunk_size=8192):
            with open(path, 'rb') as f:
                while True:
                    data = f.read(chunk_size)
                    if not data:
                        break
                    yield data

        response = StreamingHttpResponse(
            full_file_iterator(file_path),
            content_type=content_type,
        )
        response['Content-Length'] = str(file_size)

    response['Accept-Ranges'] = 'bytes'
    return response


class MovieStreamView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Stream movie video with HTTP Range support or JSON stream URLs",
        parameters=[
            OpenApiParameter('quality', str, description="Preferred quality: 360p, 480p, 720p, 1080p"),
            OpenApiParameter('format', str, description="Set 'json' to get video URLs metadata instead of binary stream"),
        ]
    )
    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id, is_active=True)
        except Movie.DoesNotExist:
            return APIResponse.error(message="Movie not found.", status_code=404)

        # Increment view count
        Movie.objects.filter(pk=movie_id).update(views=F('views') + 1)

        quality = request.query_params.get('quality')
        sources = movie.video_sources.filter(is_active=True)

        if quality:
            source = sources.filter(quality=quality).first() or sources.first()
        else:
            source = sources.first()

        # If client requested JSON metadata
        if request.query_params.get('format') == 'json' or 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            all_sources = VideoSourceSerializer(sources, many=True, context={'request': request}).data
            subtitles = SubtitleSerializer(movie.subtitles.all(), many=True, context={'request': request}).data
            return APIResponse.success(
                data={
                    "movie_id": movie.id,
                    "title": movie.title,
                    "selected_quality": source.quality if source else "default",
                    "stream_url": source.stream_url if source else movie.trailer_url,
                    "sources": all_sources,
                    "subtitles": subtitles,
                },
                message="Stream information retrieved.",
            )

        if source and source.file and os.path.exists(source.file.path):
            return range_streaming_response(request, source.file.path)
        elif source and source.source_url:
            return HttpResponseRedirect(source.source_url)
        elif movie.trailer_url:
            return HttpResponseRedirect(movie.trailer_url)

        return APIResponse.error(message="No video stream available for this movie.", status_code=404)


class EpisodeStreamView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Stream episode video with HTTP Range support")
    def get(self, request, episode_id):
        try:
            episode = Episode.objects.select_related('season__series').get(pk=episode_id, is_active=True)
        except Episode.DoesNotExist:
            return APIResponse.error(message="Episode not found.", status_code=404)

        # Increment views
        Episode.objects.filter(pk=episode_id).update(views=F('views') + 1)

        quality = request.query_params.get('quality')
        sources = episode.episode_video_sources.filter(is_active=True)

        if quality:
            source = sources.filter(quality=quality).first() or sources.first()
        else:
            source = sources.first()

        if request.query_params.get('format') == 'json' or 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            all_sources = VideoSourceSerializer(sources, many=True, context={'request': request}).data
            subtitles = SubtitleSerializer(episode.episode_subtitles.all(), many=True, context={'request': request}).data
            return APIResponse.success(
                data={
                    "episode_id": episode.id,
                    "series_title": episode.season.series.title,
                    "season_number": episode.season.season_number,
                    "episode_number": episode.episode_number,
                    "title": episode.title,
                    "stream_url": source.stream_url if source else episode.video_url,
                    "sources": all_sources,
                    "subtitles": subtitles,
                },
                message="Episode stream information retrieved.",
            )

        if source and source.file and os.path.exists(source.file.path):
            return range_streaming_response(request, source.file.path)
        elif source and source.source_url:
            return HttpResponseRedirect(source.source_url)
        elif episode.video_url:
            return HttpResponseRedirect(episode.video_url)

        return APIResponse.error(message="No video stream available for this episode.", status_code=404)


class MovieSubtitlesView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Get subtitles list for a movie")
    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id, is_active=True)
        except Movie.DoesNotExist:
            return APIResponse.error(message="Movie not found.", status_code=404)

        subtitles = movie.subtitles.all().order_by('language')
        serializer = SubtitleSerializer(subtitles, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Subtitles retrieved successfully.")


class EpisodeSubtitlesView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="Get subtitles list for an episode")
    def get(self, request, episode_id):
        try:
            episode = Episode.objects.get(pk=episode_id, is_active=True)
        except Episode.DoesNotExist:
            return APIResponse.error(message="Episode not found.", status_code=404)

        subtitles = episode.episode_subtitles.all().order_by('language')
        serializer = SubtitleSerializer(subtitles, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Subtitles retrieved successfully.")
