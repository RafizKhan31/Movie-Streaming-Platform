from django.urls import path
from .views import PlanListView, SubscribeView, MySubscriptionView

urlpatterns = [
    path('plans/', PlanListView.as_view(), name='subscription-plans'),
    path('subscribe/', SubscribeView.as_view(), name='subscription-subscribe'),
    path('my-subscription/', MySubscriptionView.as_view(), name='subscription-my'),
]
