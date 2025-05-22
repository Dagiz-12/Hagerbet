from django.db import models

from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from users.models import CustomUser
from django.utils import timezone


# profiles/models.py

from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )
    loyalty_points = models.PositiveIntegerField(default=0)
    preferred_shipping_address = models.TextField(blank=True, null=True)
    newsletter_subscription = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return f"Profile of {self.user.email}"

# Signal to create profile when user is created


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == CustomUser.Role.CUSTOMER:
        CustomerProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'customer_profile'):
        instance.customer_profile.save()
