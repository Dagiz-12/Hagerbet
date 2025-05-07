from django.urls import path
from . import views
from django.views.generic import TemplateView


app_name = 'cart'
urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('count/', views.CartCountView.as_view(), name='cart-count'),
    path('summary/', views.CartSummaryView.as_view(), name='cart-summary'),

]
