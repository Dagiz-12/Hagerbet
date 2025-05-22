from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    # Make email unique and required
    email = models.EmailField(_('email address'), unique=True)

    # Phone number
    phone = models.CharField(
        _('phone number'),
        max_length=15,
        blank=True,
        null=True,
        help_text=_('Format: +1234567890')
    )

    # Address field
    address = models.TextField(
        _('address'),
        blank=True,
        null=True,
        help_text=_('Your shipping address')
    )

    # User roles
    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', _('Customer')
        ADMIN = 'ADMIN', _('Admin')
        STAFF = 'STAFF', _('Staff')

    role = models.CharField(
        _('role'),
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER  # Default to customer
    )

    # Additional fields
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(
        _('date of birth'),
        blank=True,
        null=True,
        help_text=_('Format: YYYY-MM-DD')
    )
    # orders = models.ForeignKey(
    # 'orders.Order',
    # on_delete=models.SET_NULL,
    # null=True,
    #  blank=True,
    #   related_name='user_orders'
    # )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

# Add to users/models.py


class ActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'

    def __str__(self):
        return f"{self.user.email if self.user else 'System'} - {self.action} at {self.timestamp}"
