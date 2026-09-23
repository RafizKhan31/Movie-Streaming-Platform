from django.db import models
from django.conf import settings
from django.utils.text import slugify


class SubscriptionPlan(models.Model):
    name = models.CharField('Plan Name', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=120, unique=True)
    price = models.DecimalField('Price', max_digits=8, decimal_places=2)
    currency = models.CharField('Currency Symbol', max_length=10, default='₹')
    billing_cycle = models.CharField('Billing Cycle', max_length=50, default='per month')
    video_quality = models.CharField('Video Quality', max_length=50, default='Good (480p)')
    resolution = models.CharField('Resolution', max_length=50, default='480p')
    max_devices = models.PositiveSmallIntegerField('Devices', default=1)
    features = models.JSONField('Features List', default=list, blank=True)
    is_active = models.BooleanField('Active', default=True)

    class Meta:
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'
        ordering = ['price']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.currency}{self.price} {self.billing_cycle}"


class UserSubscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='user_subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    payment_id = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'User Subscription'
        verbose_name_plural = 'User Subscriptions'

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} (Active: {self.is_active})"
