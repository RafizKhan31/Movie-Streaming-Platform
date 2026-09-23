from rest_framework import permissions, status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from common.responses import APIResponse
from common.pagination import StandardResultsSetPagination
from apps.movies.models import Movie
from apps.tv.models import TVSeries
from .models import Review
from .serializers import ReviewSerializer


class MovieReviewsView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @extend_schema(summary="Get all reviews and ratings for a movie")
    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie_id=movie_id).select_related('user').order_by('-created_at')
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(request=ReviewSerializer, summary="Submit or update a review for a movie")
    def post(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id, is_active=True)
        except Movie.DoesNotExist:
            return APIResponse.error(message="Movie not found.", status_code=404)

        rating = request.data.get('rating')
        if not rating or not (1 <= int(rating) <= 10):
            return APIResponse.error(message="Rating must be an integer between 1 and 10.")

        title = request.data.get('title', '')
        content = request.data.get('content', '')

        # Update or create review
        review, created = Review.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={
                'rating': int(rating),
                'title': title,
                'content': content,
            }
        )

        serializer = ReviewSerializer(review, context={'request': request})
        msg = "Review submitted successfully." if created else "Review updated successfully."
        return APIResponse.success(
            data=serializer.data,
            message=msg,
            status_code=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class SeriesReviewsView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @extend_schema(summary="Get all reviews for a TV series")
    def get(self, request, series_id):
        reviews = Review.objects.filter(series_id=series_id).select_related('user').order_by('-created_at')
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(request=ReviewSerializer, summary="Submit or update review for TV series")
    def post(self, request, series_id):
        try:
            series = TVSeries.objects.get(pk=series_id, is_active=True)
        except TVSeries.DoesNotExist:
            return APIResponse.error(message="TV Series not found.", status_code=404)

        rating = request.data.get('rating')
        if not rating or not (1 <= int(rating) <= 10):
            return APIResponse.error(message="Rating must be an integer between 1 and 10.")

        title = request.data.get('title', '')
        content = request.data.get('content', '')

        review, created = Review.objects.update_or_create(
            user=request.user,
            series=series,
            defaults={
                'rating': int(rating),
                'title': title,
                'content': content,
            }
        )

        serializer = ReviewSerializer(review, context={'request': request})
        msg = "Review submitted successfully." if created else "Review updated successfully."
        return APIResponse.success(
            data=serializer.data,
            message=msg,
            status_code=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class ReviewDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Update user's own review")
    def put(self, request, pk):
        review = Review.objects.filter(pk=pk, user=request.user).first()
        if not review:
            return APIResponse.error(message="Review not found or unauthorized.", status_code=404)

        rating = request.data.get('rating')
        if rating:
            review.rating = int(rating)
        if 'title' in request.data:
            review.title = request.data.get('title')
        if 'content' in request.data:
            review.content = request.data.get('content')

        review.save()
        serializer = ReviewSerializer(review, context={'request': request})
        return APIResponse.success(data=serializer.data, message="Review updated successfully.")

    @extend_schema(summary="Delete user's own review")
    def delete(self, request, pk):
        review = Review.objects.filter(pk=pk, user=request.user).first()
        if not review:
            return APIResponse.error(message="Review not found or unauthorized.", status_code=404)

        review.delete()
        return APIResponse.success(message="Review deleted successfully.")
