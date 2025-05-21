from django.db import models
from products.models import Products
from django.conf import settings
from django.utils import timezone
import json


class Orders(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('telebirr', 'TeleBirr'),
        ('cbe_birr', 'CBE Birr'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Pending')

    # Shipping Information
    shipping_first_name = models.CharField(max_length=100)
    shipping_last_name = models.CharField(max_length=100)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zip = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=15)

    # Billing Information
    billing_first_name = models.CharField(max_length=100, blank=True)
    billing_last_name = models.CharField(max_length=100, blank=True)
    billing_address = models.TextField(blank=True)
    billing_city = models.CharField(max_length=100, blank=True)
    billing_state = models.CharField(max_length=100, blank=True)
    billing_zip = models.CharField(max_length=20, blank=True)
    billing_country = models.CharField(max_length=100, blank=True)

    # Payment
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    payment_complete = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Order Items (as JSON field)
    order_items = models.JSONField()

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"

    class Meta:
        ordering = ['-order_date']
        verbose_name_plural = 'Orders'

    @property
    def items_list(self):
        """Convert order_items JSON to proper Python list"""
        if isinstance(self.order_items, str):
            try:
                return json.loads(self.order_items)
            except json.JSONDecodeError:
                return []
        return self.order_items or []
