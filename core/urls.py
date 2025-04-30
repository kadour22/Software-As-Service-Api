from django.urls import path
from . import views

urlpatterns = [
    path('create-subscription/', views.GetSubscription.as_view(), name='subscription'),
    path('subscription/', views.SubscriptionDetailView.as_view(), name='subscription'),
    path('billing/', views.BillingListCreateView.as_view(), name='billing'),
    # path('billing/<int:billing_id>/invoice/', views.InvoiceView.as_view(), name='invoice'),
]