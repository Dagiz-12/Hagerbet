from django.db import models

from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from users.models import CustomUser
from django.utils import timezone


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile')
    loyalty_points = models.IntegerField(default=0)
    preferred_shipping_address = models.TextField(blank=True)
    newsletter_subscription = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email}'s profile"
