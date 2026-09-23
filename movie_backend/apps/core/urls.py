from django.urls import path
from .views import HomePageView, ContactView

urlpatterns = [
    path('home/', HomePageView.as_view(), name='api-home'),
    path('contact/', ContactView.as_view(), name='api-contact'),
]
