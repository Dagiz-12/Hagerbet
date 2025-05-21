from django.urls import path
from . import views

app_name = 'orders'  # This defines the namespace

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('confirmation/<int:order_id>/',
         views.OrderConfirmationView.as_view(), name='confirmation'),
]
