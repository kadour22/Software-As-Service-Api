# serializers.py
from rest_framework import serializers
from .models import Subscription, Billing


class SubscriptionSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'start_date', 'end_date', 'plan_type', 'status', 'is_active']
        read_only_fields = ['start_date', 'is_active']

    def get_is_active(self, obj):
        return obj.is_active()


class BillingSerializer(serializers.ModelSerializer):
    invoice = serializers.SerializerMethodField()

    class Meta:
        model = Billing
        fields = "__all__"
        # read_only_fields = ['billing_date', 'payment_status', 'invoice']

    def get_invoice(self, obj):
        return obj.generate_invoice()
