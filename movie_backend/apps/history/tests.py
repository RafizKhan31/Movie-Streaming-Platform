from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.movies.models import Movie
from .models import WatchHistory


class WatchHistoryAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='historyuser@example.com',
            username='historyuser',
            password='ValidPassword123!'
        )
        self.movie = Movie.objects.create(
            title='Inception',
            slug='inception-history',
            duration_minutes=120,
            is_active=True,
        )
        self.client.force_authenticate(user=self.user)
        self.history_url = reverse('history-list-create')

    def test_save_and_retrieve_history(self):
        data = {
            'movie_id': self.movie.id,
            'current_position': 2520.0, # 42 mins
            'duration': 7200.0,         # 120 mins
        }
        response = self.client.post(self.history_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['progress_percentage'], 35.0)

        # Retrieve history
        get_response = self.client.get(self.history_url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(get_response.data['data']), 1)
        self.assertEqual(get_response.data['data'][0]['progress_percentage'], 35.0)
