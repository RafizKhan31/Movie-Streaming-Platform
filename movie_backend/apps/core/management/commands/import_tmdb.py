import os
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.movies.models import Movie
from apps.genres.models import Genre


class Command(BaseCommand):
    help = "Search and import movie metadata from The Movie Database (TMDB) API"

    def add_arguments(self, parser):
        parser.add_argument('--query', type=str, help="Search title on TMDB")
        parser.add_argument('--tmdb-id', type=int, help="Direct TMDB Movie ID to import")

    def handle(self, *args, **options):
        api_key = getattr(settings, 'TMDB_API_KEY', '') or os.getenv('TMDB_API_KEY', '')
        if not api_key:
            self.stdout.write(self.style.WARNING("TMDB_API_KEY is not configured in .env. Please add TMDB_API_KEY=your_key to import live metadata from TMDB."))
            return

        base_url = "https://api.themoviedb.org/3"
        tmdb_id = options.get('tmdb_id')
        query = options.get('query')

        if not tmdb_id and not query:
            self.stdout.write(self.style.ERROR("Please provide either --query 'movie title' or --tmdb-id <id>"))
            return

        if not tmdb_id and query:
            search_url = f"{base_url}/search/movie?api_key={api_key}&query={query}"
            res = requests.get(search_url)
            if res.status_code != 200 or not res.json().get('results'):
                self.stdout.write(self.style.ERROR(f"No results found on TMDB for query: {query}"))
                return
            tmdb_id = res.json()['results'][0]['id']

        # Fetch full movie details
        detail_url = f"{base_url}/movie/{tmdb_id}?api_key={api_key}&append_to_response=credits,videos"
        detail_res = requests.get(detail_url)
        if detail_res.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Failed to fetch details for TMDB ID: {tmdb_id}"))
            return

        data = detail_res.json()
        title = data.get('title')
        overview = data.get('overview', '')
        release_date = data.get('release_date') or None
        runtime = data.get('runtime') or 120
        rating = round(data.get('vote_average', 0.0), 1)

        poster_path = data.get('poster_path')
        backdrop_path = data.get('backdrop_path')
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""
        backdrop_url = f"https://image.tmdb.org/t/p/original{backdrop_path}" if backdrop_path else ""

        # Extract trailer
        trailer_url = ""
        videos = data.get('videos', {}).get('results', [])
        for v in videos:
            if v.get('site') == 'YouTube' and v.get('type') in ('Trailer', 'Teaser'):
                trailer_url = f"https://www.youtube.com/watch?v={v.get('key')}"
                break

        hours = runtime // 60
        mins = runtime % 60
        duration_label = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"

        movie, created = Movie.objects.update_or_create(
            title=title,
            defaults={
                "description": overview,
                "release_date": release_date,
                "duration": duration_label,
                "duration_minutes": runtime,
                "imdb_rating": rating,
                "tmdb_rating": rating,
                "poster_url": poster_url,
                "backdrop_url": backdrop_url,
                "trailer_url": trailer_url,
                "is_active": True,
            }
        )

        # Link genres
        for g_item in data.get('genres', []):
            g_name = g_item.get('name')
            if g_name:
                genre_obj, _ = Genre.objects.get_or_create(name=g_name)
                movie.genres.add(genre_obj)

        action = "Imported new" if created else "Updated existing"
        self.stdout.write(self.style.SUCCESS(f"{action} movie '{movie.title}' (TMDB ID: {tmdb_id}) successfully!"))
