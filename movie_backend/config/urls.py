import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# Admin Site branding
admin.site.site_header = "The Code Wizerd Movie Site Administration"
admin.site.site_title = "Movie Streaming Admin Portal"
admin.site.index_title = "Streaming Platform Content Management"

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Authentication & User Management
    path('api/auth/', include('apps.accounts.urls')),

    # Genres & Categories
    path('api/genres/', include('apps.genres.urls')),

    # Movies Management
    path('api/movies/', include('apps.movies.urls')),

    # TV Series & Episodes
    path('api/', include('apps.tv.urls')),

    # Streaming & Subtitles
    path('api/', include('apps.streaming.urls')),

    # Watchlist & Favorites
    path('api/', include('apps.watchlist.urls')),

    # Ratings & Reviews
    path('api/', include('apps.reviews.urls')),

    # Watch History & Continue Watching
    path('api/history/', include('apps.history.urls')),

    # Unified Search
    path('api/search/', include('apps.search.urls')),

    # Subscriptions & Premium Plans
    path('api/subscriptions/', include('apps.subscriptions.urls')),

    # Core Homepage & Contact Form
    path('api/', include('apps.core.urls')),

    # API Documentation (OpenAPI 3.0 / Swagger / Redoc)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
