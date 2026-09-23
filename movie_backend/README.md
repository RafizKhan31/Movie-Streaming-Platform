# The Code Wizerd Movie Streaming Platform - Backend

A complete, production-ready backend system built with **Python 3.10+ / 3.12**, **Django**, **Django REST Framework (DRF)**, and **MySQL 8.0**. This backend powers the movie streaming website frontend, providing authentication, content delivery, video streaming with HTTP Range requests, multi-language subtitles, user engagement features (watchlist, favorites, reviews), watch history with continue-watching progress, subscription plans, and unified search.

---

## 📑 Table of Contents

- [Architecture & Tech Stack](#-architecture--tech-stack)
- [Database Schema & Models](#-database-schema--models)
- [Quick Start & Local Setup](#-quick-start--local-setup)
- [Environment Configuration](#-environment-configuration)
- [Running Celery & Background Tasks](#-running-celery--background-tasks)
- [Docker & Containerized Deployment](#-docker--containerized-deployment)
- [API Endpoints Reference](#-api-endpoints-reference)
- [Video Streaming & Range Requests](#-video-streaming--range-requests)
- [Frontend Integration Guide](#-frontend-integration-guide)
- [Testing & Quality Assurance](#-testing--quality-assurance)
- [Default Demo Credentials](#-default-demo-credentials)

---

## 🏛 Architecture & Tech Stack

```
                        ┌─────────────────────────────────────┐
                        │      Existing HTML5 / JS Client     │
                        │  (home.html, movie-min.html, etc.)  │
                        └──────────────────┬──────────────────┘
                                           │
                                    REST API / JWT
                                  (js/api.js Client)
                                           │
                                           ▼
                        ┌─────────────────────────────────────┐
                        │          Nginx Reverse Proxy        │
                        │     (Static & Media File Caching)   │
                        └──────────────────┬──────────────────┘
                                           │
                                           ▼
                        ┌─────────────────────────────────────┐
                        │         Gunicorn / Django API       │
                        │   Django REST Framework + SimpleJWT │
                        └──┬───────────────┬────────────────┬─┘
                           │               │                │
            Django ORM / PyMySQL           │           Celery Worker
                           │               │           & Redis Cache
                           ▼               ▼                ▼
                     ┌──────────┐    ┌──────────┐     ┌───────────┐
                     │ MySQL 8  │    │  Redis   │     │  Celery   │
                     │ Database │    │  Cache   │     │   Tasks   │
                     └──────────┘    └──────────┘     └───────────┘
```

- **Backend Framework**: Django 5.x & Django REST Framework (DRF)
- **Database**: MySQL 8.0 (UTF-8 MB4 charset, InnoDB storage engine)
- **Database Driver**: PyMySQL (configured as MySQLdb)
- **Authentication**: JWT (JSON Web Tokens) via `djangorestframework-simplejwt`
- **Cache & Task Broker**: Redis 7.x
- **Asynchronous Tasks**: Celery 5.x
- **API Documentation**: OpenAPI 3.0 via `drf-spectacular` (Swagger UI & ReDoc)
- **Image Processing**: Pillow
- **Containerization**: Docker & Docker Compose with multi-stage builds and Nginx

---

## 🗄 Database Schema & Models

The system is organized into modular Django apps:

1. **`apps.accounts`**:
   - `User`: Custom user model inheriting from `AbstractUser` with email login (`USERNAME_FIELD = 'email'`), `avatar`, `phone_number`, `bio`, `date_of_birth`, and timestamp fields.

2. **`apps.genres`**:
   - `Genre`: Movie/series genres (`Action`, `Drama`, `Comedy`, etc.) with slug, icon, and description.

3. **`apps.movies`**:
   - `Person`: Actors, directors, and creators.
   - `Movie`: Feature films with title, slug, description, release year, duration, age rating, IMDb rating, poster, backdrop, trailer URL, view count, and featured/trending flags.
   - `MovieCast`: M2M through model linking `Movie` and `Person` with character name and role type.
   - `MovieSubmission`: User-submitted movie suggestions with poster uploads, email, and approval status (`pending`, `approved`, `rejected`).

4. **`apps.tv`**:
   - `TVSeries`: Multi-season television series with status (`ongoing`, `ended`), ratings, poster, and trailer.
   - `Season`: Season number, title, overview, poster, and air date.
   - `Episode`: Episode number, title, description, duration, thumbnail, and view counts.

5. **`apps.streaming`**:
   - `VideoSource`: Video streams attached to movies or episodes with quality (`360p`, `480p`, `720p`, `1080p`, `4k`), format (`mp4`, `hls`, `dash`), direct file upload or CDN URL.
   - `Subtitle`: Multilingual subtitles (English, Bengali, Hindi, etc.) in `.vtt` or `.srt` formats.

6. **`apps.watchlist`**:
   - `Watchlist`: User saved content (movies or series) with unique constraints per user and item.
   - `Favorite`: Quick favorited content.

7. **`apps.reviews`**:
   - `Review`: User rating (1 to 10 scale) and written review text. Includes unique constraints preventing duplicate reviews and signals that automatically recalculate the movie/series average rating.

8. **`apps.history`**:
   - `WatchHistory`: Playback progress tracking (`current_position`, `duration`, `completed`, `progress_percentage`, `last_watched_at`) for "Continue Watching" rails.

9. **`apps.subscriptions`**:
   - `SubscriptionPlan`: Tiered plans (Basic, Standard, Premium) with price, max stream quality, simultaneous screens, and downloads.
   - `UserSubscription`: Active user subscription with expiry date and renewal tracking.

10. **`apps.core`**:
    - `ContactInquiry`: Contact form messages submitted from the frontend.

---

## 🚀 Quick Start & Local Setup

### 1. Prerequisites
- Python 3.10 or 3.12 installed
- MySQL Server 8.0 running locally
- (Optional) Redis server for caching and Celery tasks

### 2. Clone and Setup Environment

```bash
# Navigate to the backend directory
cd d:/Project/movie/movie_backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. MySQL Configuration
Ensure MySQL has a database named `movie_streaming_db` created with UTF-8 support:

```sql
CREATE DATABASE IF NOT EXISTS movie_streaming_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Update your `.env` file with your MySQL credentials:
```env
DB_NAME=movie_streaming_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 4. Run Migrations and Seed Data

```bash
# Run database migrations
python manage.py migrate

# Populate database with realistic movies, TV series, genres, video sources, subtitles, and demo users
python manage.py seed_data
```

### 5. Start the Server

```bash
python manage.py runserver 127.0.0.1:8000
```

The API will now be accessible at:
- **API Base URL**: `http://127.0.0.1:8000/api/`
- **Swagger Documentation**: `http://127.0.0.1:8000/api/docs/`
- **OpenAPI Schema**: `http://127.0.0.1:8000/api/schema/`
- **Django Admin**: `http://127.0.0.1:8000/admin/`

---

## ⚙ Environment Configuration

Create a `.env` file in `movie_backend/` (or copy from `.env.example`):

```ini
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-goes-here
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=movie_streaming_db
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306

CORS_ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
CORS_ALLOW_ALL_ORIGINS=True

JWT_ACCESS_LIFETIME=60
JWT_REFRESH_LIFETIME=1440

REDIS_URL=redis://127.0.0.1:6379/1
CELERY_BROKER_URL=redis://127.0.0.1:6379/0

TMDB_API_KEY=
```

---

## ⚡ Running Celery & Background Tasks

Celery handles periodic and asynchronous tasks such as TMDB catalog syncs, sending email notifications, and cleaning up expired watch tokens.

```bash
# Start Celery Worker
celery -A config worker -l info --pool=threads

# Start Celery Beat Scheduler (in another terminal)
celery -A config beat -l info
```

---

## 🐳 Docker & Containerized Deployment

Run the complete multi-container stack (Django, MySQL, Redis, Celery Worker, Celery Beat, Nginx) with a single command:

```bash
# From d:/Project/movie/movie_backend:
docker compose up -d --build
```

To view logs:
```bash
docker compose logs -f backend
```

To stop containers:
```bash
docker compose down
```

---

## 📡 API Endpoints Reference

All API responses follow a uniform format:
```json
{
  "success": true,
  "message": "Human-readable status message",
  "data": { ... }
}
```

### 1. Authentication (`/api/auth/`)
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/auth/register/` | Public | Register new user account |
| `POST` | `/api/auth/login/` | Public | Login with email & password, returns JWT tokens |
| `POST` | `/api/auth/token/refresh/` | Public | Refresh expired access token |
| `POST` | `/api/auth/logout/` | JWT | Blacklist refresh token & logout |
| `GET` | `/api/auth/profile/` | JWT | Get current user profile |
| `PUT/PATCH` | `/api/auth/profile/` | JWT | Update user profile & avatar |
| `POST` | `/api/auth/change-password/` | JWT | Change current password |
| `POST` | `/api/auth/forgot-password/` | Public | Request password reset token |
| `POST` | `/api/auth/reset-password/` | Public | Set new password using token |

### 2. Homepage & Core (`/api/`)
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/home/` | Optional | Curated homepage data: featured, trending, popular, latest, continue-watching |
| `POST` | `/api/contact/` | Public | Submit contact form inquiry |

### 3. Genres (`/api/genres/`)
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/genres/` | Public | List all available genres |
| `GET` | `/api/genres/{slug}/` | Public | Genre details |
| `GET` | `/api/genres/{slug}/movies/`| Public | Movies in a specific genre |

### 4. Movies (`/api/movies/`)
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/movies/` | Public | Filtered and paginated movies list |
| `GET` | `/api/movies/{id_or_slug}/` | Public | Movie details with cast, genres, ratings |
| `GET` | `/api/movies/trending/` | Public | Trending movies (sorted by views/rating) |
| `GET` | `/api/movies/popular/` | Public | Popular movies |
| `GET` | `/api/movies/latest/` | Public | Latest movie releases |
| `GET` | `/api/movies/featured/` | Public | Admin-curated featured movies |
| `GET` | `/api/movies/top-rated/` | Public | Top IMDb-rated movies |
| `POST` | `/api/movies/submit/` | Public | User movie submission form |

### 5. TV Series & Episodes (`/api/tv/` or `/api/series/`)
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/tv/` | Public | List TV series |
| `GET` | `/api/tv/{id_or_slug}/` | Public | TV Series details |
| `GET` | `/api/tv/{id}/seasons/` | Public | List seasons for a TV series |
| `GET` | `/api/tv/{id}/episodes/` | Public | List episodes (filter by `?season=X`) |
| `GET` | `/api/episodes/{id}/` | Public | Episode details |

### 6. Video Streaming & Subtitles (`/api/`)
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/movies/{id}/stream/` | Public | Stream movie video with HTTP Range (`206`) or JSON metadata (`?format=json`) |
| `GET` | `/api/episodes/{id}/stream/` | Public | Stream episode video with HTTP Range (`206`) or JSON metadata |
| `GET` | `/api/movies/{id}/subtitles/`| Public | List subtitles for a movie |
| `GET` | `/api/episodes/{id}/subtitles/`| Public| List subtitles for an episode |

### 7. Watchlist & Favorites (`/api/`)
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/watchlist/` | JWT | Get user's saved watchlist |
| `POST` | `/api/watchlist/` | JWT | Add movie or TV series to watchlist |
| `DELETE` | `/api/watchlist/{id}/` | JWT | Remove item from watchlist |
| `GET` | `/api/favorites/` | JWT | Get user's favorites |
| `POST` | `/api/favorites/` | JWT | Add item to favorites |
| `DELETE` | `/api/favorites/{id}/` | JWT | Remove item from favorites |

### 8. Ratings & Reviews (`/api/reviews/`)
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/reviews/?movie_id=X` | Public | List user reviews for a movie |
| `POST` | `/api/reviews/` | JWT | Submit a review and 1-10 rating |
| `PUT/PATCH` | `/api/reviews/{id}/` | JWT | Update user's existing review |
| `DELETE` | `/api/reviews/{id}/` | JWT | Delete user's review |

### 9. Watch History & Progress (`/api/history/`)
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/history/` | JWT | List watch history (Continue Watching) |
| `POST` | `/api/history/progress/` | JWT | Save playback progress (`position`, `duration`) |
| `DELETE` | `/api/history/{id}/` | JWT | Clear item from history |

### 10. Unified Search (`/api/search/`)
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/search/?q={query}` | Public | Search across movies, series, cast, and genres |

### 11. Subscriptions (`/api/subscriptions/`)
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/subscriptions/plans/` | Public | List available subscription tiers |
| `GET` | `/api/subscriptions/current/` | JWT | Current user subscription status |
| `POST` | `/api/subscriptions/subscribe/` | JWT | Subscribe to a plan |

---

## 🎬 Video Streaming & Range Requests

Video streaming supports standard HTTP Range requests (`RFC 7233`), enabling HTML5 `<video>` tags to seek forward/backward instantly without waiting for the full file download.

### How it works:
1. Browser sends request with header: `Range: bytes=1048576-`
2. Django backend validates and opens the video file, seeking directly to byte `1048576`.
3. Backend returns **`206 Partial Content`** with headers:
   ```http
   HTTP/1.1 206 Partial Content
   Content-Type: video/mp4
   Accept-Ranges: bytes
   Content-Range: bytes 1048576-2097151/52428800
   Content-Length: 1048576
   ```
4. Subtitles are dynamically attached as `<track kind="subtitles" srclang="en" label="English" src="...">` in HTML5 format (`.vtt`).

---

## 🌐 Frontend Integration Guide

The frontend connects to the backend through `js/api.js`. This library automatically:
- Manages JWT access and refresh tokens in `localStorage`.
- Automatically refreshes tokens transparently upon HTTP `401 Unauthorized` responses.
- Augments the navbar with dynamic user greeting, Login/Logout buttons, Profile modal, and Watchlist modal.
- Provides a video player modal (`api.ui.openPlayer(options)`) that streams high-quality video, switches resolutions on the fly, switches subtitle tracks (English, Bengali, Hindi), and automatically posts progress ticks to `POST /api/history/progress/` every 10 seconds.
- Connects search inputs on all pages (`#searchForm`) to `/api/search/?q=...`.

### Sample Usage in Frontend:
```javascript
// Check if user is logged in
if (api.isAuthenticated()) {
    const user = api.getUser();
    console.log("Logged in as:", user.username);
}

// Fetch movies
const res = await api.movies.list({ genre: 'action', page: 1 });
if (res.success) {
    console.log("Movies found:", res.data.results);
}

// Open video streaming modal with subtitles
api.ui.openPlayer({
    movieId: 1,
    title: "Inception",
    videoUrl: "http://127.0.0.1:8000/api/movies/1/stream/",
    subtitles: [
        { label: "English", srclang: "en", file_url: "..." },
        { label: "Bengali", srclang: "bn", file_url: "..." }
    ]
});
```

---

## 🧪 Testing & Quality Assurance

Run the automated test suite with Django's test runner:

```bash
python manage.py test
```

All 14 core test cases test registration, JWT login, movie retrieval, watchlist duplicate prevention, and watch history calculations.

To run end-to-end endpoint verification against the live server:
```bash
python scratch/test_api_endpoints.py
```

---

## 🔑 Default Demo Credentials

After running `python manage.py seed_data`:

| Role | Email | Password | Permissions |
|---|---|---|---|
| **Superuser / Admin** | `admin@moviesite.com` | `admin123` | Full Django Admin & Staff access |
| **Demo User** | `demo@moviesite.com` | `Password123!` | Standard streaming user with seed history & watchlist |
