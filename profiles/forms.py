
from django import forms
from .models import CustomerProfile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = [
            'preferred_shipping_address',
            'newsletter_subscription'
        ]
        widgets = {
            'preferred_shipping_address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter your complete shipping address'
            }),
        }
