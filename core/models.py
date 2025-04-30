from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import timezone 
from django.utils.timezone import now
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    start_date = models.DateField(auto_now_add=True)
    end_date   = models.DateField(null=True, blank=True)
    plan_type  = models.CharField(max_length=50) 
    status     = models.CharField(max_length=20, default='active')

    def __str__(self):
        return f"{self.user.username}'s Subscription"

    def is_active(self):
        return self.status == 'active' and self.end_date >= timezone.now().date()

    def renew(self, new_end_date):
        self.end_date = new_end_date
        self.save()

    def cancel(self):
        self.status = 'canceled'
        self.save()

class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount         = models.DecimalField(max_digits=10, decimal_places=2)
    billing_date   = models.DateField()
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ] , default='pending')

    def process_payment(self):
        try:
      
            if self.amount > 0:
                self.payment_status = 'completed'
            else:
                self.payment_status = 'failed'
            self.billing_date = now().date()
            self.save()
        except Exception as e:
            self.payment_status = 'failed'
            self.save()
            raise Exception(f"Payment processing failed: {str(e)}")

    def generate_invoice(self):
        invoice_id = uuid.uuid4()  
        invoice    = (
            f"Invoice ID: {invoice_id}\n"
            f"User: {self.user.username}\n"
            f"Amount: ${self.amount}\n"
            f"Billing Date: {self.billing_date}\n"
            f"Payment Status: {self.payment_status}\n"
        )
        return invoice

    def __str__(self):
        return f'Billing for {self.user.username} - Amount: {self.amount}'
