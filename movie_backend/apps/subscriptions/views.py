from datetime import timedelta
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from common.responses import APIResponse
from .models import SubscriptionPlan, UserSubscription
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer


class PlanListView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="List all available subscription plans")
    def get(self, request):
        plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return APIResponse.success(data=serializer.data, message="Subscription plans retrieved.")


class SubscribeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=UserSubscriptionSerializer, summary="Subscribe user to a plan")
    def post(self, request):
        plan_id = request.data.get('plan_id')
        payment_id = request.data.get('payment_id', 'DEMO_PAYMENT_OK')

        try:
            plan = SubscriptionPlan.objects.get(pk=plan_id, is_active=True)
        except SubscriptionPlan.DoesNotExist:
            return APIResponse.error(message="Invalid subscription plan selected.")

        now = timezone.now()
        end_date = now + timedelta(days=30)

        sub, created = UserSubscription.objects.update_or_create(
            user=request.user,
            defaults={
                'plan': plan,
                'start_date': now,
                'end_date': end_date,
                'is_active': True,
                'payment_id': payment_id,
            }
        )

        request.user.is_premium = True
        request.user.save(update_fields=['is_premium'])

        serializer = UserSubscriptionSerializer(sub)
        return APIResponse.success(
            data=serializer.data,
            message=f"Successfully subscribed to {plan.name} plan!",
            status_code=status.HTTP_201_CREATED,
        )


class MySubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Get current user's active subscription")
    def get(self, request):
        sub = UserSubscription.objects.filter(user=request.user, is_active=True).select_related('plan').first()
        if not sub:
            return APIResponse.success(data=None, message="No active subscription found.")
        serializer = UserSubscriptionSerializer(sub)
        return APIResponse.success(data=serializer.data, message="Current subscription retrieved.")
