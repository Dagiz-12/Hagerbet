from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.CartView.as_view(), name='view'),
    path('add/<int:product_id>/', views.AddToCartView.as_view(),
         name='add_to_cart'),  # Changed name
    path('update/<int:product_id>/', views.UpdateCartView.as_view(), name='update'),
    path('remove/<int:product_id>/',
         views.RemoveFromCartView.as_view(), name='remove'),
    path('count/', views.CartCountView.as_view(), name='count'),
]
