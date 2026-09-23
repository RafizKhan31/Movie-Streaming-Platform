from django.urls import path
from .views import WatchHistoryView, WatchHistoryDetailView

urlpatterns = [
    path('', WatchHistoryView.as_view(), name='history-list-create'),
    path('<int:pk>/', WatchHistoryDetailView.as_view(), name='history-detail'),
]
