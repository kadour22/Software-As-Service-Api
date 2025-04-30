
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Subscription, Billing
from .serializers import SubscriptionSerializer, BillingSerializer
from datetime import timedelta
from django.utils import timezone

from .utils import generate_invoice_pdf

class GetSubscription(generics.CreateAPIView) :
    serializer_class = SubscriptionSerializer

class SubscriptionDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.subscription

    def patch(self, request, *args, **kwargs):
        action = request.data.get("action")
        subscription = self.get_object()

        if action == "renew":
            extra_days = int(request.data.get("days", 30))
            new_end_date = subscription.end_date + timedelta(days=extra_days)
            subscription.renew(new_end_date)
            return Response({"detail": "Subscription renewed."}, status=status.HTTP_200_OK)

        elif action == "cancel":
            subscription.cancel()
            return Response({"detail": "Subscription canceled."}, status=status.HTTP_200_OK)

        return super().patch(request, *args, **kwargs)


class BillingListCreateView(generics.ListCreateAPIView):
    serializer_class = BillingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Billing.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        billing = serializer.save(user=self.request.user)
        billing.process_payment()
        generate_invoice_pdf(billing)

