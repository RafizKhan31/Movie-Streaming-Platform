import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from apps.accounts.models import User
from apps.genres.models import Genre
from apps.movies.models import Person, Movie, MovieCast
from apps.tv.models import TVSeries, Season, Episode
from apps.streaming.models import VideoSource, Subtitle
from apps.reviews.models import Review
from apps.history.models import WatchHistory
from apps.subscriptions.models import SubscriptionPlan, UserSubscription


class Command(BaseCommand):
    help = "Seed database with realistic movie, tv series, genres, cast, streaming video sources, subtitles, and test users"

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding...")

        # 1. Test Users
        admin_user, _ = User.objects.get_or_create(
            email="admin@moviesite.com",
            defaults={
                "username": "admin",
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
                "is_premium": True,
            }
        )
        admin_user.set_password("admin123")
        admin_user.save()
        self.stdout.write("Created/updated Superuser: admin@moviesite.com / admin123")

        demo_user, _ = User.objects.get_or_create(
            email="demo@moviesite.com",
            defaults={
                "username": "demo_user",
                "first_name": "Rafiz",
                "last_name": "Khan",
                "is_staff": False,
                "is_superuser": False,
                "is_premium": True,
            }
        )
        demo_user.set_password("Password123!")
        demo_user.save()
        self.stdout.write("Created/updated Demo User: demo@moviesite.com / Password123!")

        # 2. Subscription Plans
        plans_data = [
            {
                "name": "Basic",
                "slug": "basic",
                "price": 499.00,
                "currency": "₹",
                "billing_cycle": "per month",
                "video_quality": "Good",
                "resolution": "480p",
                "max_devices": 1,
                "features": ["Video Quality: Good", "Resolution: 480p", "Devices: Mobile, Tablet"],
            },
            {
                "name": "Standard",
                "slug": "standard",
                "price": 699.00,
                "currency": "₹",
                "billing_cycle": "per month",
                "video_quality": "Better",
                "resolution": "1080p",
                "max_devices": 2,
                "features": ["Video Quality: Better", "Resolution: 1080p", "Devices: Mobile, Tablet, TV, PC"],
            },
            {
                "name": "Premium",
                "slug": "premium",
                "price": 999.00,
                "currency": "₹",
                "billing_cycle": "per month",
                "video_quality": "Best (Ultra HD)",
                "resolution": "4K+HDR",
                "max_devices": 4,
                "features": ["Video Quality: Best (Ultra HD)", "Resolution: 4K+HDR", "Devices: All devices", "Spatial Audio"],
            },
        ]
        for p in plans_data:
            plan, _ = SubscriptionPlan.objects.update_or_create(slug=p['slug'], defaults=p)

        # 3. Genres
        genres_data = [
            ("Action", "action", "fa-fire"),
            ("Crime", "crime", "fa-user-secret"),
            ("Suspense & Thriller", "suspense", "fa-mask"),
            ("Sci-Fi & Fantasy", "fantasy", "fa-rocket"),
            ("Documentary", "documentary", "fa-film"),
            ("Horror", "horror", "fa-ghost"),
            ("Drama", "drama", "fa-theater-masks"),
            ("War & Politics", "war", "fa-shield-alt"),
            ("Comedy", "comedy", "fa-laugh"),
            ("Romance", "romance", "fa-heart"),
            ("Anime", "anime", "fa-tv"),
            ("Kids", "kids", "fa-child"),
            ("Popular", "popular", "fa-star"),
        ]
        genre_objs = {}
        for name, slug, icon in genres_data:
            g, _ = Genre.objects.get_or_create(slug=slug, defaults={"name": name, "icon": icon})
            genre_objs[slug] = g
        self.stdout.write(f"Seeded {len(genre_objs)} genres.")

        # 4. People (Cast & Directors)
        people_data = [
            ("Christopher Nolan", "director", "Acclaimed filmmaker known for mind-bending blockbusters."),
            ("Leonardo DiCaprio", "actor", "Oscar-winning actor renowned for versatile leading roles."),
            ("Christian Bale", "actor", "Transformative British-American method actor."),
            ("Heath Ledger", "actor", "Legendary actor who portrayed the iconic Joker."),
            ("Sushant Singh Rajput", "actor", "Beloved Indian actor celebrated for his inspiring performances."),
            ("Ranbir Kapoor", "actor", "Leading Bollywood actor and performer."),
            ("Aamir Khan", "actor", "Trailblazing Indian actor, director and perfectionist."),
            ("Bryan Cranston", "actor", "Multi-Emmy award winning star of Breaking Bad."),
            ("Aaron Paul", "actor", "Emmy-winning actor famous for Jesse Pinkman."),
            ("Peter Dinklage", "actor", "Award-winning actor famous for Tyrion Lannister in Game of Thrones."),
            ("Pankaj Tripathi", "actor", "Critically acclaimed Indian actor beloved for Mirzapur."),
            ("Nawazuddin Siddiqui", "actor", "Acclaimed global actor renowned for Sacred Games."),
            ("Pratik Gandhi", "actor", "Star of Scam 1992 portraying Harshad Mehta."),
        ]
        people_objs = {}
        for name, role, bio in people_data:
            p, _ = Person.objects.get_or_create(name=name, defaults={"role": role, "bio": bio})
            people_objs[name] = p

        # 5. Movies
        movies_data = [
            {
                "title": "Inception",
                "slug": "inception",
                "description": "Cobb steals information from his targets by entering their dreams. Saito offers to wipe clean Cobb's criminal history as payment for performing an inception on his sick competitor's son.",
                "poster_url": "Images/inception.jpg",
                "backdrop_url": "Images/inception.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=YoHD9XEInc0",
                "release_year": 2010,
                "duration": "2h 42m",
                "duration_minutes": 162,
                "imdb_rating": 8.8,
                "category": "hollywood",
                "featured": True,
                "trending": True,
                "genres": ["fantasy", "suspense", "action"],
                "directors": ["Christopher Nolan"],
                "cast": [("Leonardo DiCaprio", "Dom Cobb", 1)],
            },
            {
                "title": "The Dark Knight",
                "slug": "the-dark-knight",
                "description": "After Gordon, Dent and Batman begin an assault on Gotham's organised crime, the mobs hire the Joker, a psychopathic criminal mastermind who offers to kill Batman and bring the city to its knees.",
                "poster_url": "Images/dark knight.jpg",
                "backdrop_url": "Images/dark knight.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=LDG9bisJEaI",
                "release_year": 2008,
                "duration": "2h 32m",
                "duration_minutes": 152,
                "imdb_rating": 9.0,
                "category": "hollywood",
                "featured": True,
                "trending": True,
                "genres": ["action", "crime", "drama"],
                "directors": ["Christopher Nolan"],
                "cast": [("Christian Bale", "Bruce Wayne / Batman", 1), ("Heath Ledger", "Joker", 2)],
            },
            {
                "title": "MS Dhoni: The Untold Story",
                "slug": "ms-dhoni-the-untold-story",
                "description": "A chronicle of the inspiring journey of Indian cricket team captain Mahendra Singh Dhoni, from a small-town railway ticket collector to lifting the World Cup for India.",
                "poster_url": "Images/msdhoni.jpg",
                "backdrop_url": "Images/msd.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=6L6XqWoS8tw",
                "release_year": 2016,
                "duration": "3h 10m",
                "duration_minutes": 190,
                "imdb_rating": 8.5,
                "category": "bollywood",
                "featured": True,
                "trending": True,
                "genres": ["drama"],
                "cast": [("Sushant Singh Rajput", "M.S. Dhoni", 1)],
            },
            {
                "title": "Yeh Jawaani Hai Deewani",
                "slug": "yeh-jawaani-hai-deewani",
                "description": "Kabir and Naina bond during a trekking trip. Before Naina can express her feelings, Kabir leaves India to pursue his career. Years later, they reunite at a friend's wedding.",
                "poster_url": "Images/ye jawani.jpg",
                "backdrop_url": "Images/YJHD cover.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=Rbp2XUSeUNE",
                "release_year": 2013,
                "duration": "2h 40m",
                "duration_minutes": 160,
                "imdb_rating": 9.0,
                "category": "bollywood",
                "featured": True,
                "trending": True,
                "genres": ["romance", "comedy", "drama"],
                "cast": [("Ranbir Kapoor", "Kabir Thapar (Bunny)", 1)],
            },
            {
                "title": "3 Idiots",
                "slug": "3-idiots",
                "description": "Two friends embark on a quest for a lost buddy. On this journey, they reminisce about their college days and the memory of their friend who inspired them to think differently.",
                "poster_url": "Images/Idiots.png",
                "backdrop_url": "Images/Idiots.png",
                "trailer_url": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
                "release_year": 2009,
                "duration": "2h 50m",
                "duration_minutes": 170,
                "imdb_rating": 9.0,
                "category": "bollywood",
                "featured": True,
                "trending": True,
                "genres": ["comedy", "drama"],
                "cast": [("Aamir Khan", "Rancho / Phunsukh Wangdu", 1)],
            },
            {
                "title": "Bajrangi Bhaijaan",
                "slug": "bajrangi-bhaijaan",
                "description": "An Indian man with a magnanimous heart takes a mute Pakistani girl back to her hometown to reunite her with her family across the border.",
                "poster_url": "Images/bb.jpg",
                "backdrop_url": "Images/bb.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=4nwAra0mz_Q",
                "release_year": 2015,
                "duration": "2h 43m",
                "duration_minutes": 163,
                "imdb_rating": 8.7,
                "category": "bollywood",
                "trending": True,
                "genres": ["drama", "comedy", "action"],
                "cast": [("Nawazuddin Siddiqui", "Chand Nawab", 2)],
            },
            {
                "title": "Pati Patni Aur Woh",
                "slug": "pati-patni-aur-woh",
                "description": "Chintu Tyagi is an ordinary, middle-class man who finds himself torn between his wife and another woman, leading to comical chaos and drama.",
                "poster_url": "Images/ppw.jpg",
                "backdrop_url": "Images/ppw.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=L7T44vBYfFU",
                "release_year": 2019,
                "duration": "2h 08m",
                "duration_minutes": 128,
                "imdb_rating": 8.0,
                "category": "bollywood",
                "genres": ["comedy", "romance"],
            },
            {
                "title": "Holiday: A Soldier Is Never Off Duty",
                "slug": "holiday-a-soldier-is-never-off-duty",
                "description": "A military officer on leave hunts down a terrorist sleeper cell network in Mumbai to prevent a series of devastating bomb blasts across the city.",
                "poster_url": "Images/holiday.jpg",
                "backdrop_url": "Images/holiday.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=13F1P9c6zM0",
                "release_year": 2014,
                "duration": "2h 50m",
                "duration_minutes": 170,
                "imdb_rating": 8.1,
                "category": "bollywood",
                "genres": ["action", "thriller"],
            },
            {
                "title": "Brave",
                "slug": "brave",
                "description": "Determined to make her own path in life, Princess Merida defies a custom that brings chaos to her kingdom. Granted one wish, Merida must rely on her bravery and archery skills to undo a beastly curse.",
                "poster_url": "images/p1.jpg",
                "backdrop_url": "images/p1.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=TEHWDA_6e3M",
                "release_year": 2012,
                "duration": "1h 33m",
                "duration_minutes": 93,
                "imdb_rating": 7.1,
                "category": "kids",
                "genres": ["kids", "fantasy", "comedy"],
            },
            {
                "title": "The Hobbit: An Unexpected Journey",
                "slug": "the-hobbit-an-unexpected-journey",
                "description": "A reluctant Hobbit, Bilbo Baggins, sets out to the Lonely Mountain with a spirited group of dwarves to reclaim their mountain home and the gold within it from the dragon Smaug.",
                "poster_url": "images/p2.jpg",
                "backdrop_url": "images/p2.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=nOGsB9dORBg",
                "release_year": 2012,
                "duration": "2h 49m",
                "duration_minutes": 169,
                "imdb_rating": 7.8,
                "category": "hollywood",
                "genres": ["fantasy", "action"],
            },
            {
                "title": "Tenet",
                "slug": "tenet",
                "description": "Armed with only one word, Tenet, and fighting for the survival of the entire world, a Protagonist journeys through a twilight world of international espionage on a mission that will unfold in something beyond real time.",
                "poster_url": "Images/tenet.jpg",
                "backdrop_url": "Images/tenet.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=L3pk_TBkihU",
                "release_year": 2020,
                "duration": "2h 30m",
                "duration_minutes": 150,
                "imdb_rating": 7.8,
                "category": "hollywood",
                "genres": ["action", "fantasy", "suspense"],
                "directors": ["Christopher Nolan"],
            },
            {
                "title": "Dangal",
                "slug": "dangal",
                "description": "Former wrestler Mahavir Singh Phogat and his two wrestler daughters struggle towards glory at the Commonwealth Games in the face of societal oppression.",
                "poster_url": "Images/dangal.jpg",
                "backdrop_url": "Images/dangal.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=x_7YlGv9u1g",
                "release_year": 2016,
                "duration": "2h 41m",
                "duration_minutes": 161,
                "imdb_rating": 8.4,
                "category": "bollywood",
                "genres": ["drama", "action"],
                "cast": [("Aamir Khan", "Mahavir Singh Phogat", 1)],
            },
        ]

        # Sample webvtt subtitles
        sample_vtt_en = "WEBVTT\n\n1\n00:00:01.000 --> 00:00:04.000\nWelcome to The Code Wizerd Movie Site!\n\n2\n00:00:05.000 --> 00:00:09.000\nStreaming in high definition with multi-language subtitle support.\n"
        sample_vtt_bn = "WEBVTT\n\n1\n00:00:01.000 --> 00:00:04.000\nদ্য কোড উইজার্ড মুভি সাইটে স্বাগতম!\n\n2\n00:00:05.000 --> 00:00:09.000\nবাংলা সাবটাইটেল সহ উপভোগ করুন আপনার প্রিয় সিনেমা।\n"
        sample_vtt_hi = "WEBVTT\n\n1\n00:00:01.000 --> 00:00:04.000\nद कोड विज़ार्ड मूवी साइट पर आपका स्वागत है!\n\n2\n00:00:05.000 --> 00:00:09.000\nहिंदी सबटाइटल के साथ बेहतरीन स्ट्रीमिंग का आनंद लें।\n"

        # Public CDN streaming video demo (Big Buck Bunny / Blender Open Movie for seamless playback testing)
        demo_stream_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

        for m_data in movies_data:
            genres_list = m_data.pop("genres", [])
            directors_list = m_data.pop("directors", [])
            cast_list = m_data.pop("cast", [])

            movie, _ = Movie.objects.update_or_create(slug=m_data['slug'], defaults=m_data)

            for g_slug in genres_list:
                if g_slug in genre_objs:
                    movie.genres.add(genre_objs[g_slug])

            for d_name in directors_list:
                if d_name in people_objs:
                    movie.directors.add(people_objs[d_name])

            for p_name, char_name, order in cast_list:
                if p_name in people_objs:
                    MovieCast.objects.update_or_create(
                        movie=movie,
                        person=people_objs[p_name],
                        defaults={"character_name": char_name, "order": order},
                    )

            # Create video sources
            VideoSource.objects.get_or_create(
                movie=movie,
                quality="720p",
                defaults={"source_url": demo_stream_url, "is_active": True},
            )
            VideoSource.objects.get_or_create(
                movie=movie,
                quality="1080p",
                defaults={"source_url": demo_stream_url, "is_active": True},
            )

            # Create subtitles
            sub_en, _ = Subtitle.objects.get_or_create(
                movie=movie,
                language="en",
                defaults={"label": "English", "is_default": True},
            )
            if not sub_en.subtitle_file:
                sub_en.subtitle_file.save(f"{movie.slug}_en.vtt", ContentFile(sample_vtt_en.encode('utf-8')))

            sub_bn, _ = Subtitle.objects.get_or_create(
                movie=movie,
                language="bn",
                defaults={"label": "Bengali", "is_default": False},
            )
            if not sub_bn.subtitle_file:
                sub_bn.subtitle_file.save(f"{movie.slug}_bn.vtt", ContentFile(sample_vtt_bn.encode('utf-8')))

        self.stdout.write(f"Seeded {len(movies_data)} movies with streaming sources and subtitles.")

        # 6. TV Series
        series_data = [
            {
                "title": "Breaking Bad",
                "slug": "breaking-bad",
                "description": "A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine with a former student in order to secure his family's future.",
                "poster_url": "Images/breaking.jpg",
                "backdrop_url": "Images/breaking.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=HhesaQXLuRY",
                "release_year": 2008,
                "imdb_rating": 9.5,
                "category": "tv_series",
                "featured": True,
                "trending": True,
                "genres": ["crime", "drama", "suspense"],
                "cast": ["Bryan Cranston", "Aaron Paul"],
                "episodes_count": 7,
            },
            {
                "title": "Game of Thrones",
                "slug": "game-of-thrones",
                "description": "Nine noble families fight for control over the lands of Westeros, while an ancient enemy returns after being dormant for millennia.",
                "poster_url": "Images/got.jpg",
                "backdrop_url": "Images/got.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=KPLWWIOCOOQ",
                "release_year": 2011,
                "imdb_rating": 9.2,
                "category": "tv_series",
                "featured": True,
                "trending": True,
                "genres": ["fantasy", "drama", "action"],
                "cast": ["Peter Dinklage"],
                "episodes_count": 10,
            },
            {
                "title": "Sacred Games",
                "slug": "sacred-games",
                "description": "A link in their pasts leads an honest cop to a fugitive gang boss, whose cryptic warning spurs the officer on a quest to save Mumbai from cataclysm.",
                "poster_url": "Images/sacred.jpg",
                "backdrop_url": "Images/sacred.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=28j8h0RRnq4",
                "release_year": 2018,
                "imdb_rating": 8.6,
                "category": "web_series",
                "trending": True,
                "genres": ["crime", "suspense", "drama"],
                "cast": ["Nawazuddin Siddiqui", "Pankaj Tripathi"],
                "episodes_count": 8,
            },
            {
                "title": "Mirzapur",
                "slug": "mirzapur",
                "description": "A shocking incident at a wedding procession ignites a series of events entangling two families in the lawless city of Mirzapur.",
                "poster_url": "Images/mirzapur.jpg",
                "backdrop_url": "Images/mirzapur.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=ZNeGF-PvVHY",
                "release_year": 2018,
                "imdb_rating": 8.5,
                "category": "web_series",
                "trending": True,
                "genres": ["crime", "action", "drama"],
                "cast": ["Pankaj Tripathi"],
                "episodes_count": 9,
            },
            {
                "title": "Kota Factory",
                "slug": "kota-factory",
                "description": "Dedicated to the students of Kota, the series depicts the life and struggles of students preparing for IIT-JEE in India's educational coaching hub.",
                "poster_url": "Images/kota.jpg",
                "backdrop_url": "Images/kota.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=pNZQ6msbO2Q",
                "release_year": 2019,
                "imdb_rating": 9.0,
                "category": "web_series",
                "genres": ["comedy", "drama"],
                "episodes_count": 5,
            },
            {
                "title": "Scam 1992: The Harshad Mehta Story",
                "slug": "scam-1992",
                "description": "Set in 1980s and 90s Bombay, it follows the life of Harshad Mehta, a stockbroker who took the stock market to dizzying heights and his catastrophic downfall.",
                "poster_url": "Images/scam.jpg",
                "backdrop_url": "Images/scam.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=ISORfez27og",
                "release_year": 2020,
                "imdb_rating": 9.3,
                "category": "web_series",
                "genres": ["drama", "crime"],
                "cast": ["Pratik Gandhi"],
                "episodes_count": 10,
            },
            {
                "title": "Apharan",
                "slug": "apharan",
                "description": "A story of kidnapping, suspense, mystery, and conspiracy set in the heart of Uttarakhand, driven by crime and corruption.",
                "poster_url": "Images/apharan.jpg",
                "backdrop_url": "Images/apharan.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=fX-6xX98d34",
                "release_year": 2018,
                "imdb_rating": 8.3,
                "category": "web_series",
                "genres": ["suspense", "crime", "action"],
                "episodes_count": 12,
            },
        ]

        for s_data in series_data:
            genres_list = s_data.pop("genres", [])
            cast_list = s_data.pop("cast", [])
            episodes_count = s_data.pop("episodes_count", 5)

            series, _ = TVSeries.objects.update_or_create(slug=s_data['slug'], defaults=s_data)

            for g_slug in genres_list:
                if g_slug in genre_objs:
                    series.genres.add(genre_objs[g_slug])

            for p_name in cast_list:
                if p_name in people_objs:
                    series.cast.add(people_objs[p_name])

            # Create Season 1
            season1, _ = Season.objects.get_or_create(
                series=series,
                season_number=1,
                defaults={"title": "Season 1", "description": f"First season of {series.title}"}
            )

            # Create episodes
            for ep_num in range(1, episodes_count + 1):
                ep, _ = Episode.objects.get_or_create(
                    season=season1,
                    episode_number=ep_num,
                    defaults={
                        "title": f"Episode {ep_num}",
                        "description": f"Thrilling episode {ep_num} of {series.title}.",
                        "duration": "50m",
                        "duration_minutes": 50,
                        "video_url": demo_stream_url,
                    }
                )

                # Episode video source
                VideoSource.objects.get_or_create(
                    episode=ep,
                    quality="720p",
                    defaults={"source_url": demo_stream_url, "is_active": True},
                )

        self.stdout.write(f"Seeded {len(series_data)} TV Series with seasons and episodes.")

        # 7. Reviews & Ratings
        Review.objects.update_or_create(
            user=demo_user,
            movie=Movie.objects.get(slug="inception"),
            defaults={
                "rating": 10,
                "title": "A Cinematic Masterpiece!",
                "content": "Mind-bending visual storytelling at its peak. The rotating hallway fight scene is iconic.",
            }
        )
        Review.objects.update_or_create(
            user=admin_user,
            movie=Movie.objects.get(slug="the-dark-knight"),
            defaults={
                "rating": 10,
                "title": "Unrivaled Superhero Film",
                "content": "Heath Ledger's performance is unforgettable. One of the best movies of all time.",
            }
        )

        # 8. Watch History (Continue Watching) for demo user
        inc_movie = Movie.objects.get(slug="inception")
        WatchHistory.objects.update_or_create(
            user=demo_user,
            movie=inc_movie,
            defaults={
                "current_position": 2520.0,  # 42 minutes
                "duration": 9720.0,          # 162 minutes
                "completed": False,
            }
        )
        bb_series = TVSeries.objects.get(slug="breaking-bad")
        first_ep = Episode.objects.filter(season__series=bb_series).first()
        if first_ep:
            WatchHistory.objects.update_or_create(
                user=demo_user,
                episode=first_ep,
                defaults={
                    "current_position": 1080.0,  # 18 minutes
                    "duration": 3000.0,          # 50 minutes
                    "completed": False,
                }
            )

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
