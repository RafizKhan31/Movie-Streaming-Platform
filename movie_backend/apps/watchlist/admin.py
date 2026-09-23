from django.contrib import admin
from .models import Watchlist, Favorite


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'series', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'movie__title', 'series__title')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'series', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'movie__title', 'series__title')
