from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id',
            'name',
            'slug',
            'price',
            'currency',
            'billing_cycle',
            'video_quality',
            'resolution',
            'max_devices',
            'features',
            'is_active',
        ]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=SubscriptionPlan.objects.all(), source='plan', write_only=True
    )

    class Meta:
        model = UserSubscription
        fields = ['id', 'plan', 'plan_id', 'start_date', 'end_date', 'is_active', 'payment_id']
        read_only_fields = ['id', 'start_date', 'end_date', 'is_active']
