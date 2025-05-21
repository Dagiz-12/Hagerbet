from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'dashboard'

urlpatterns = [
    path('', views.HomeView.as_view(), name='dashboard'),
    path('orders/', views.OrderHistoryView.as_view(), name='order_history'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update/',
         views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/process/<str:action>/',
         views.process_order, name='process_order'),
    path('orders/<int:pk>/receipt/',
         views.generate_receipt_pdf, name='generate_receipt'),
]
