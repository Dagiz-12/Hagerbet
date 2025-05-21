from django import forms
from django.core.validators import RegexValidator
from .models import Orders


class CheckoutForm(forms.Form):
    # Shipping Information
    shipping_first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    shipping_last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    shipping_address = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street Address'})
    )
    shipping_city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    shipping_state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'State/Region'})
    )
    shipping_zip = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Postal/Zip Code'})
    )
    shipping_country = forms.ChoiceField(
        choices=[('ET', 'Ethiopia')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    shipping_phone = forms.CharField(
        max_length=15,
        validators=[RegexValidator(
            r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )

    # Billing Information (checkbox to copy from shipping)
    same_billing_address = forms.BooleanField(
        required=False,
        initial=True,
        label='Billing address same as shipping',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    billing_first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    billing_last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    billing_address = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street Address'})
    )
    billing_city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    billing_state = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'State/Region'})
    )
    billing_zip = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Postal/Zip Code'})
    )
    billing_country = forms.ChoiceField(
        required=False,
        choices=[('ET', 'Ethiopia')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Payment Method
    payment_method = forms.ChoiceField(
        choices=Orders.PAYMENT_METHODS,
        widget=forms.RadioSelect(attrs={'class': 'payment-method-radio'})
    )

    # Payment Details (shown based on selection)
    card_number = forms.CharField(
        max_length=19,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '1234 5678 9012 3456'})
    )
    card_expiry = forms.CharField(
        max_length=7,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'MM/YYYY'})
    )
    card_cvv = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'CVV'})
    )
    card_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Name on Card'})
    )
    telebirr_phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'TeleBirr Phone Number'})
    )
    cbe_birr_account = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'CBE Account Number'})
    )

    # Terms and conditions
    accept_terms = forms.BooleanField(
        required=True,
        label='I agree to the Terms and Conditions',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
