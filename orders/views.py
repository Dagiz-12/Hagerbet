import requests

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from cart.utils import get_cart, clear_cart
from .models import Orders
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import CheckoutForm
import json
from django.core.mail import send_mail
from django.conf import settings


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'orders/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('orders:confirmation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_cart(self.request)

        cart_items = []
        total_price = 0

        for product_id, item_data in cart.cart.items():
            item_total = float(item_data['price']) * item_data['quantity']
            cart_items.append({
                'id': product_id,
                **item_data,
                'total': item_total
            })
            total_price += item_total

        context['cart_items'] = cart_items
        context['total_price'] = total_price
        return context

    def form_valid(self, form):
        cart = get_cart(self.request)
        cart_items = []
        total_price = 0

        for product_id, item_data in cart.cart.items():
            item_total = float(item_data['price']) * item_data['quantity']
            cart_items.append({
                'product_id': product_id,
                'name': item_data['name'],
                'price': item_data['price'],
                'quantity': item_data['quantity'],
                'image': item_data['image'],
                'total': item_total
            })
            total_price += item_total

        # Create order
        order = Orders.objects.create(
            user=self.request.user,
            shipping_first_name=form.cleaned_data['shipping_first_name'],
            shipping_last_name=form.cleaned_data['shipping_last_name'],
            shipping_address=form.cleaned_data['shipping_address'],
            shipping_city=form.cleaned_data['shipping_city'],
            shipping_state=form.cleaned_data['shipping_state'],
            shipping_zip=form.cleaned_data['shipping_zip'],
            shipping_country=form.cleaned_data['shipping_country'],
            shipping_phone=form.cleaned_data['shipping_phone'],
            billing_first_name=form.cleaned_data['billing_first_name'] if not form.cleaned_data[
                'same_billing_address'] else form.cleaned_data['shipping_first_name'],
            billing_last_name=form.cleaned_data['billing_last_name'] if not form.cleaned_data[
                'same_billing_address'] else form.cleaned_data['shipping_last_name'],
            billing_address=form.cleaned_data['billing_address'] if not form.cleaned_data[
                'same_billing_address'] else form.cleaned_data['shipping_address'],
            billing_city=form.cleaned_data['billing_city'] if not form.cleaned_data[
                'same_billing_address'] else form.cleaned_data['shipping_city'],
            billing_state=form.cleaned_data['billing_state'] if not form.cleaned_data[
                'same_billing_address'] else form.cleaned_data['shipping_state'],
            billing_zip=form.cleaned_data['billing_zip'] if not form.cleaned_data[
                'same_billing_address'] else form.cleaned_data['shipping_zip'],
            billing_country=form.cleaned_data['billing_country'] if not form.cleaned_data[
                'same_billing_address'] else form.cleaned_data['shipping_country'],
            payment_method=form.cleaned_data['payment_method'],
            total_price=total_price,
            order_items=json.dumps(cart_items)
        )

        # Process payment based on method
        payment_method = form.cleaned_data['payment_method']
        if payment_method == 'paypal':
            # Implement PayPal integration here
            pass
        elif payment_method == 'telebirr':
            # Implement TeleBirr integration here
            pass
        elif payment_method == 'cbe_birr':
            # Implement CBE Birr integration here
            pass

        # Clear cart
        clear_cart(self.request)

        # Send confirmation email
        send_mail(
            f'Order #{order.id} Confirmation',
            f'Thank you for your order! Your order number is {order.id}.',
            settings.DEFAULT_FROM_EMAIL,
            [self.request.user.email],
            fail_silently=False,
        )

        # Redirect to confirmation page with order ID
        return redirect('orders:confirmation', order_id=order.id)


class OrderConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')
        context['order'] = Orders.objects.get(
            id=order_id, user=self.request.user)
        return context


# paypal pyament


# def process_paypal_payment(order, request):
 #   paypalrestsdk.configure({
  #      "mode": "sandbox",  # Change to "live" for production
   #     "client_id": settings.PAYPAL_CLIENT_ID,
    #    "client_secret": settings.PAYPAL_SECRET
    # })

    # payment = paypalrestsdk.Payment({
     #   "intent": "sale",
      #  "payer": {
       #     "payment_method": "paypal"
       # },
        # "transactions": [{
        #   "amount": {
        #      "total": str(order.total_price),
        #     "currency": "USD"
        # },
        # "description": f"Order #{order.id}"
       # }],
        # "redirect_urls": {
        #   "return_url": request.build_absolute_uri(reverse('orders:paypal_success')),
        #   "cancel_url": request.build_absolute_uri(reverse('orders:paypal_cancel'))
        # }
   # })

    # if payment.create():
     #   return payment.links[1].href  # Redirect to PayPal approval URL
    # else:
     #   raise Exception(payment.error)

# TeleBirr payment processing


def process_telebirr_payment(order, phone_number):
    # Replace with actual TeleBirr API endpoint
    url = "https://api.telebirr.com/payment"
    payload = {
        "amount": str(order.total_price),
        "currency": "ETB",
        "customer_phone": phone_number,
        "order_id": str(order.id),
        "callback_url": settings.TELEBIRR_CALLBACK_URL
    }

    headers = {
        "Authorization": f"Bearer {settings.TELEBIRR_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get('payment_url')
    else:
        raise Exception("TeleBirr payment failed")
