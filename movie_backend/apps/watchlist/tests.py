from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.movies.models import Movie
from .models import Watchlist, Favorite


class WatchlistAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='watchlistuser@example.com',
            username='watchlistuser',
            password='ValidPassword123!'
        )
        self.movie = Movie.objects.create(
            title='Interstellar',
            slug='interstellar',
            release_year=2014,
            imdb_rating=8.7,
            is_active=True,
        )
        self.client.force_authenticate(user=self.user)
        self.watchlist_url = reverse('watchlist-list-create')
        self.favorites_url = reverse('favorites-list-create')

    def test_add_to_watchlist(self):
        data = {'movie_id': self.movie.id}
        response = self.client.post(self.watchlist_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Watchlist.objects.filter(user=self.user, movie=self.movie).count(), 1)

    def test_watchlist_duplicate_prevention(self):
        data = {'movie_id': self.movie.id}
        self.client.post(self.watchlist_url, data, format='json')
        # Post again
        response = self.client.post(self.watchlist_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Watchlist.objects.filter(user=self.user, movie=self.movie).count(), 1)

    def test_delete_from_watchlist(self):
        item = Watchlist.objects.create(user=self.user, movie=self.movie)
        delete_url = reverse('watchlist-delete', kwargs={'pk': item.id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Watchlist.objects.filter(user=self.user).count(), 0)

    def test_favorites(self):
        data = {'movie_id': self.movie.id}
        response = self.client.post(self.favorites_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favorite.objects.filter(user=self.user, movie=self.movie).count(), 1)
