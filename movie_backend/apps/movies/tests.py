from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.genres.models import Genre
from .models import Movie


class MovieAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name='Action', slug='action')
        self.movie = Movie.objects.create(
            title='Inception',
            slug='inception',
            description='A mind-bending thriller.',
            release_year=2010,
            imdb_rating=8.8,
            category='hollywood',
            featured=True,
            trending=True,
            is_active=True,
        )
        self.movie.genres.add(self.genre)

    def test_movie_list(self):
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertGreaterEqual(response.data['data']['count'], 1)

    def test_movie_filter_by_genre(self):
        url = reverse('movie-list')
        response = self.client.get(url, {'genre': 'action'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['count'], 1)

    def test_movie_detail(self):
        url = reverse('movie-detail', kwargs={'identifier': 'inception'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['title'], 'Inception')

    def test_movie_trending(self):
        url = reverse('movie-trending')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['data']), 1)
